/**
 * Authentication Service
 * 
 * Handles all authentication API calls to the backend.
 * Uses fetch with credentials: 'include' for HttpOnly cookie support.
 */

// API base URL - hardcoded for development, can be configured via build
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Check if we're running in browser
const isBrowser = typeof window !== 'undefined';

// Types
export interface User {
  id: number;
  email: string;
  created_at: string;
  last_login?: string;
}

export interface UserProfile {
  id: number;
  user_id: number;
  programming_level: string;
  robotics_familiarity: string;
  hardware_experience: string;
  learning_goal: string;
  updated_at: string;
}

export interface UserWithProfile extends User {
  profile?: UserProfile;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface ProfileRequest {
  programming_level: 'none' | 'beginner' | 'intermediate' | 'advanced';
  robotics_familiarity: 'none' | 'hobbyist' | 'academic' | 'professional';
  hardware_experience: 'none' | 'arduino' | 'embedded' | 'industrial';
  learning_goal: 'career_change' | 'academic' | 'hobby' | 'professional_dev';
}

export interface AuthResponse {
  message: string;
  user: User;
}

export interface ApiError {
  detail: string;
  code?: string;
}

/**
 * Helper function to handle API responses
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: `HTTP ${response.status}: ${response.statusText}`,
    }));
    throw new Error(error.detail || 'An error occurred');
  }
  return response.json();
}

/**
 * Register a new user
 */
export async function register(data: RegisterRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Include cookies
    body: JSON.stringify(data),
  });
  return handleResponse<AuthResponse>(response);
}

/**
 * Login with email and password
 */
export async function login(data: LoginRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse<AuthResponse>(response);
}

/**
 * Logout and clear session
 */
export async function logout(): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  return handleResponse<{ message: string }>(response);
}

/**
 * Refresh access token using refresh token
 */
export async function refreshToken(): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    credentials: 'include',
  });
  return handleResponse<AuthResponse>(response);
}

/**
 * Get current authenticated user
 */
export async function getCurrentUser(): Promise<UserWithProfile> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: 'GET',
    credentials: 'include',
  });
  return handleResponse<UserWithProfile>(response);
}

/**
 * Create user profile (after registration)
 */
export async function createProfile(data: ProfileRequest): Promise<UserProfile> {
  const response = await fetch(`${API_BASE_URL}/user/profile`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse<UserProfile>(response);
}

/**
 * Update existing user profile
 */
export async function updateProfile(data: ProfileRequest): Promise<UserProfile> {
  const response = await fetch(`${API_BASE_URL}/user/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse<UserProfile>(response);
}

/**
 * Get user profile
 */
export async function getProfile(): Promise<UserProfile> {
  const response = await fetch(`${API_BASE_URL}/user/profile`, {
    method: 'GET',
    credentials: 'include',
  });
  return handleResponse<UserProfile>(response);
}

export default {
  register,
  login,
  logout,
  refreshToken,
  getCurrentUser,
  createProfile,
  updateProfile,
  getProfile,
};
