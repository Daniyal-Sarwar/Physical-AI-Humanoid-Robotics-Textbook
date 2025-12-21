/**
 * Authentication Context
 * 
 * Provides global authentication state and methods for the entire app.
 * Handles login, logout, registration, and token refresh.
 */

import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import * as authService from '../../services/authService';
import type { UserWithProfile, ProfileRequest } from '../../services/authService';

interface AuthState {
  user: UserWithProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  createProfile: (profile: ProfileRequest) => Promise<void>;
  updateProfile: (profile: ProfileRequest) => Promise<void>;
  clearError: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Token refresh interval (14 minutes - before 15 min access token expires)
const REFRESH_INTERVAL = 14 * 60 * 1000;

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Refresh user data from server
  const refreshUser = useCallback(async () => {
    try {
      const user = await authService.getCurrentUser();
      setState(prev => ({
        ...prev,
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }));
    } catch (err) {
      // Not authenticated - this is expected for anonymous users
      setState(prev => ({
        ...prev,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      }));
    }
  }, []);

  // Check authentication on mount
  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  // Set up token refresh interval
  useEffect(() => {
    if (!state.isAuthenticated) return;

    const refreshTimer = setInterval(async () => {
      try {
        await authService.refreshToken();
      } catch (err) {
        // Token refresh failed - user needs to re-login
        setState(prev => ({
          ...prev,
          user: null,
          isAuthenticated: false,
          error: 'Session expired. Please sign in again.',
        }));
      }
    }, REFRESH_INTERVAL);

    return () => clearInterval(refreshTimer);
  }, [state.isAuthenticated]);

  const login = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const response = await authService.login({ email, password });
      setState({
        user: response.user as UserWithProfile,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
      // Fetch full user data with profile
      await refreshUser();
    } catch (err) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: err instanceof Error ? err.message : 'Login failed',
      }));
      throw err;
    }
  }, [refreshUser]);

  const register = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const response = await authService.register({ email, password });
      setState({
        user: response.user as UserWithProfile,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: err instanceof Error ? err.message : 'Registration failed',
      }));
      throw err;
    }
  }, []);

  const logout = useCallback(async () => {
    setState(prev => ({ ...prev, isLoading: true }));
    try {
      await authService.logout();
    } catch (err) {
      // Ignore logout errors - clear state anyway
    }
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  }, []);

  const createProfile = useCallback(async (profile: ProfileRequest) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const newProfile = await authService.createProfile(profile);
      setState(prev => ({
        ...prev,
        user: prev.user ? { ...prev.user, profile: newProfile } : null,
        isLoading: false,
      }));
    } catch (err) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: err instanceof Error ? err.message : 'Failed to create profile',
      }));
      throw err;
    }
  }, []);

  const updateProfile = useCallback(async (profile: ProfileRequest) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const updatedProfile = await authService.updateProfile(profile);
      setState(prev => ({
        ...prev,
        user: prev.user ? { ...prev.user, profile: updatedProfile } : null,
        isLoading: false,
      }));
    } catch (err) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: err instanceof Error ? err.message : 'Failed to update profile',
      }));
      throw err;
    }
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    createProfile,
    updateProfile,
    clearError,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access authentication context
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
