/**
 * Sign In Modal
 * 
 * Modal dialog for user authentication with email and password.
 */

import React, { useState, FormEvent } from 'react';
import { useAuth } from './AuthContext';
import styles from './AuthModals.module.css';

interface SignInModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSwitchToSignUp: () => void;
}

export function SignInModal({ isOpen, onClose, onSwitchToSignUp }: SignInModalProps) {
  const { login, isLoading, error, clearError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    clearError();

    // Basic validation
    if (!email || !password) {
      setLocalError('Please enter both email and password');
      return;
    }

    try {
      await login(email, password);
      onClose();
      // Reset form
      setEmail('');
      setPassword('');
    } catch (err) {
      // Error is handled by AuthContext
    }
  };

  const handleClose = () => {
    setLocalError(null);
    clearError();
    setEmail('');
    setPassword('');
    onClose();
  };

  const displayError = localError || error;

  return (
    <div className={styles.modalOverlay} onClick={handleClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={handleClose} aria-label="Close">
          ×
        </button>
        
        <h2 className={styles.modalTitle}>Sign In</h2>
        <p className={styles.modalSubtitle}>
          Sign in to access unlimited chatbot interactions
        </p>

        {displayError && (
          <div className={styles.errorMessage}>
            {displayError}
          </div>
        )}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="signin-email" className={styles.label}>
              Email
            </label>
            <input
              id="signin-email"
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className={styles.input}
              placeholder="you@example.com"
              autoComplete="email"
              disabled={isLoading}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="signin-password" className={styles.label}>
              Password
            </label>
            <input
              id="signin-password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className={styles.input}
              placeholder="••••••••"
              autoComplete="current-password"
              disabled={isLoading}
              required
            />
          </div>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className={styles.switchPrompt}>
          Don't have an account?{' '}
          <button
            type="button"
            className={styles.switchButton}
            onClick={onSwitchToSignUp}
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}

export default SignInModal;
