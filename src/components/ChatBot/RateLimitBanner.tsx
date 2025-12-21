/**
 * Rate Limit Banner Component
 * 
 * Shows remaining requests for anonymous users and prompts to sign up.
 */

import React from 'react';
import { RateLimitStatus, formatResetTime } from '../../services/rateLimitService';
import styles from './RateLimitBanner.module.css';

interface RateLimitBannerProps {
  status: RateLimitStatus | null;
  onSignUpClick: () => void;
}

export function RateLimitBanner({ status, onSignUpClick }: RateLimitBannerProps) {
  if (!status || status.is_authenticated) {
    return null;
  }

  const remaining = status.remaining;
  const total = status.total;
  const percentage = (remaining / total) * 100;
  
  const isLow = remaining <= 2;
  const isExhausted = remaining === 0;

  if (isExhausted) {
    return (
      <div className={`${styles.banner} ${styles.exhausted}`}>
        <div className={styles.content}>
          <svg className={styles.icon} width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path 
              d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" 
              stroke="currentColor" 
              strokeWidth="1.5"
            />
            <path d="M10 6V10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            <circle cx="10" cy="13" r="1" fill="currentColor"/>
          </svg>
          <div className={styles.text}>
            <span className={styles.title}>Daily limit reached</span>
            <span className={styles.subtitle}>
              Sign up for unlimited access. Resets {formatResetTime(status.reset_at)}
            </span>
          </div>
        </div>
        <button className={styles.signUpButton} onClick={onSignUpClick}>
          Sign Up Free
        </button>
      </div>
    );
  }

  if (isLow) {
    return (
      <div className={`${styles.banner} ${styles.warning}`}>
        <div className={styles.content}>
          <svg className={styles.icon} width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path 
              d="M8.57465 3.21667L1.51632 14.5C1.37079 14.7519 1.29379 15.0376 1.29298 15.3286C1.29216 15.6196 1.36756 15.9057 1.51171 16.1585C1.65585 16.4113 1.8637 16.622 2.11444 16.7696C2.36519 16.9172 2.64999 16.9966 2.94098 17H17.0577C17.3487 16.9966 17.6335 16.9172 17.8842 16.7696C18.135 16.622 18.3428 16.4113 18.487 16.1585C18.6311 15.9057 18.7065 15.6196 18.7057 15.3286C18.7049 15.0376 18.6279 14.7519 18.4823 14.5L11.424 3.21667C11.2754 2.97174 11.0657 2.76872 10.8157 2.62808C10.5658 2.48744 10.2844 2.41389 9.99898 2.41389C9.71357 2.41389 9.43217 2.48744 9.18224 2.62808C8.93231 2.76872 8.72259 2.97174 8.57398 3.21667H8.57465Z" 
              stroke="currentColor" 
              strokeWidth="1.5" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            />
            <path d="M10 7.5V10.8333" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            <circle cx="10" cy="13.75" r="0.833" fill="currentColor"/>
          </svg>
          <div className={styles.text}>
            <span className={styles.title}>
              {remaining} question{remaining !== 1 ? 's' : ''} remaining today
            </span>
            <span className={styles.subtitle}>
              Sign up for unlimited access
            </span>
          </div>
        </div>
        <div className={styles.progressBar}>
          <div 
            className={styles.progressFill} 
            style={{ width: `${percentage}%` }}
          />
        </div>
        <button className={styles.signUpLink} onClick={onSignUpClick}>
          Sign Up →
        </button>
      </div>
    );
  }

  // Normal state - just show counter
  return (
    <div className={styles.banner}>
      <div className={styles.content}>
        <svg className={styles.icon} width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path 
            d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" 
            stroke="currentColor" 
            strokeWidth="1.5"
          />
          <path d="M10 6V10L13 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
        <span className={styles.counter}>
          {remaining}/{total} questions remaining
        </span>
      </div>
      <button className={styles.signUpLink} onClick={onSignUpClick}>
        Get unlimited →
      </button>
    </div>
  );
}

export default RateLimitBanner;
