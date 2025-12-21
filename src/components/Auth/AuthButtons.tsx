/**
 * Auth Buttons Component
 * 
 * Navigation bar buttons for Sign In / Sign Up or user menu when authenticated.
 */

import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import { SignInModal } from './SignInModal';
import { SignUpModal } from './SignUpModal';
import { Questionnaire } from './Questionnaire';
import { ProfileSettings } from './ProfileSettings';
import styles from './AuthButtons.module.css';

type ModalState = 'none' | 'signin' | 'signup' | 'questionnaire' | 'profile';

export function AuthButtons() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [modalState, setModalState] = useState<ModalState>('none');
  const [showUserMenu, setShowUserMenu] = useState(false);

  if (isLoading) {
    return (
      <div className={styles.authButtons}>
        <div className={styles.loadingDot} />
      </div>
    );
  }

  const handleSignInClick = () => setModalState('signin');
  const handleSignUpClick = () => setModalState('signup');
  const closeModals = () => setModalState('none');
  
  const switchToSignIn = () => setModalState('signin');
  const switchToSignUp = () => setModalState('signup');
  
  const handleRegistrationComplete = () => {
    setModalState('questionnaire');
  };
  
  const handleQuestionnaireComplete = () => {
    setModalState('none');
  };

  const handleLogout = async () => {
    setShowUserMenu(false);
    await logout();
  };

  if (isAuthenticated && user) {
    return (
      <div className={styles.authButtons}>
        <div className={styles.userMenuContainer}>
          <button
            className={styles.userButton}
            onClick={() => setShowUserMenu(!showUserMenu)}
            aria-expanded={showUserMenu}
          >
            <span className={styles.userAvatar}>
              {user.email.charAt(0).toUpperCase()}
            </span>
            <span className={styles.userEmail}>{user.email}</span>
            <svg 
              className={`${styles.chevron} ${showUserMenu ? styles.chevronUp : ''}`}
              width="12" 
              height="12" 
              viewBox="0 0 12 12"
            >
              <path 
                d="M2 4L6 8L10 4" 
                stroke="currentColor" 
                strokeWidth="2" 
                fill="none"
              />
            </svg>
          </button>
          
          {showUserMenu && (
            <div className={styles.userMenu}>
              <div className={styles.menuHeader}>
                <span className={styles.menuEmail}>{user.email}</span>
                {user.profile && (
                  <span className={styles.menuProfile}>
                    {user.profile.programming_level} • {user.profile.learning_goal.replace('_', ' ')}
                  </span>
                )}
              </div>
              <hr className={styles.menuDivider} />
              <button 
                className={styles.menuItem} 
                onClick={() => {
                  setShowUserMenu(false);
                  setModalState('profile');
                }}
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path 
                    d="M8 8C9.65685 8 11 6.65685 11 5C11 3.34315 9.65685 2 8 2C6.34315 2 5 3.34315 5 5C5 6.65685 6.34315 8 8 8ZM8 9C5.79086 9 2 10.1193 2 12.5V14H14V12.5C14 10.1193 10.2091 9 8 9Z" 
                    stroke="currentColor" 
                    strokeWidth="1.5" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  />
                </svg>
                Edit Profile
              </button>
              <button className={styles.menuItem} onClick={handleLogout}>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path 
                    d="M6 14H3C2.44772 14 2 13.5523 2 13V3C2 2.44772 2.44772 2 3 2H6M11 11L14 8M14 8L11 5M14 8H6" 
                    stroke="currentColor" 
                    strokeWidth="1.5" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  />
                </svg>
                Sign Out
              </button>
            </div>
          )}
        </div>

        {/* Modals */}
        <ProfileSettings
          isOpen={modalState === 'profile'}
          onClose={closeModals}
        />
        <Questionnaire
          isOpen={modalState === 'questionnaire'}
          onComplete={handleQuestionnaireComplete}
          onSkip={handleQuestionnaireComplete}
        />
      </div>
    );
  }

  return (
    <div className={styles.authButtons}>
      <button 
        className={styles.signInButton}
        onClick={handleSignInClick}
      >
        Sign In
      </button>
      <button 
        className={styles.signUpButton}
        onClick={handleSignUpClick}
      >
        Sign Up
      </button>

      {/* Modals */}
      <SignInModal
        isOpen={modalState === 'signin'}
        onClose={closeModals}
        onSwitchToSignUp={switchToSignUp}
      />
      <SignUpModal
        isOpen={modalState === 'signup'}
        onClose={closeModals}
        onSwitchToSignIn={switchToSignIn}
        onRegistrationComplete={handleRegistrationComplete}
      />
      <Questionnaire
        isOpen={modalState === 'questionnaire'}
        onComplete={handleQuestionnaireComplete}
        onSkip={handleQuestionnaireComplete}
      />
    </div>
  );
}

export default AuthButtons;
