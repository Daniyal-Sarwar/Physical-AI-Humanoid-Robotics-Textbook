/**
 * Sign Up Modal
 * 
 * Modal dialog for user registration with email and password.
 * Transitions to Questionnaire after successful registration.
 */

import React, { useState, FormEvent } from 'react';
import { useAuth } from './AuthContext';
import styles from './AuthModals.module.css';

interface SignUpModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSwitchToSignIn: () => void;
  onRegistrationComplete: () => void; // Triggers questionnaire
}

export function SignUpModal({ 
  isOpen, 
  onClose, 
  onSwitchToSignIn,
  onRegistrationComplete 
}: SignUpModalProps) {
  const { register, isLoading, error, clearError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  if (!isOpen) return null;

  const validatePassword = (pwd: string): string | null => {
    if (pwd.length < 8) {
      return 'Password must be at least 8 characters';
    }
    if (!/[A-Za-z]/.test(pwd)) {
      return 'Password must contain at least one letter';
    }
    if (!/[0-9]/.test(pwd)) {
      return 'Password must contain at least one number';
    }
    return null;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    clearError();

    // Validation
    if (!email || !password || !confirmPassword) {
      setLocalError('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      setLocalError('Passwords do not match');
      return;
    }

    const passwordError = validatePassword(password);
    if (passwordError) {
      setLocalError(passwordError);
      return;
    }

    try {
      await register(email, password);
      // Reset form
      setEmail('');
      setPassword('');
      setConfirmPassword('');
      // Trigger questionnaire
      onRegistrationComplete();
    } catch (err) {
      // Error is handled by AuthContext
    }
  };

  const handleClose = () => {
    setLocalError(null);
    clearError();
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    onClose();
  };

  const displayError = localError || error;

  return (
    <div className={styles.modalOverlay} onClick={handleClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={handleClose} aria-label="Close">
          ×
        </button>
        
        <h2 className={styles.modalTitle}>Create Account</h2>
        <p className={styles.modalSubtitle}>
          Sign up for unlimited access to the AI learning assistant
        </p>

        {displayError && (
          <div className={styles.errorMessage}>
            {displayError}
          </div>
        )}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="signup-email" className={styles.label}>
              Email
            </label>
            <input
              id="signup-email"
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
            <label htmlFor="signup-password" className={styles.label}>
              Password
            </label>
            <input
              id="signup-password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className={styles.input}
              placeholder="At least 8 characters"
              autoComplete="new-password"
              disabled={isLoading}
              required
            />
            <span className={styles.hint}>
              Must contain letters and numbers
            </span>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="signup-confirm" className={styles.label}>
              Confirm Password
            </label>
            <input
              id="signup-confirm"
              type="password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              className={styles.input}
              placeholder="Repeat password"
              autoComplete="new-password"
              disabled={isLoading}
              required
            />
          </div>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <div className={styles.switchPrompt}>
          Already have an account?{' '}
          <button
            type="button"
            className={styles.switchButton}
            onClick={onSwitchToSignIn}
          >
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
}

export default SignUpModal;
