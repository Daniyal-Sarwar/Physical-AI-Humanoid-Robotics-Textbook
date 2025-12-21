/**
 * Root Theme Wrapper
 * 
 * This component wraps the entire Docusaurus app to provide:
 * - AuthContext for global authentication state
 * - ChatBot floating widget
 * - Navbar auth buttons injection
 */

import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { AuthProvider } from '@site/src/components/Auth/AuthContext';
import { ChatBot } from '@site/src/components/ChatBot/ChatBot';
import { AuthButtons } from '@site/src/components/Auth/AuthButtons';
import { SignUpModal } from '@site/src/components/Auth/SignUpModal';
import { SignInModal } from '@site/src/components/Auth/SignInModal';
import { Questionnaire } from '@site/src/components/Auth/Questionnaire';

interface Props {
  children: React.ReactNode;
}

function NavbarAuthInjector() {
  const [container, setContainer] = useState<HTMLElement | null>(null);

  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;
    
    // Find navbar right items container
    const findNavbar = () => {
      const navbarItems = document.querySelector('.navbar__items--right');
      if (navbarItems) {
        // Create container for auth buttons if it doesn't exist
        let authContainer = document.getElementById('navbar-auth-buttons');
        if (!authContainer) {
          authContainer = document.createElement('div');
          authContainer.id = 'navbar-auth-buttons';
          authContainer.style.display = 'flex';
          authContainer.style.alignItems = 'center';
          authContainer.style.marginLeft = '0.5rem';
          navbarItems.appendChild(authContainer);
        }
        setContainer(authContainer);
      }
    };

    // Try immediately and observe for changes
    findNavbar();
    
    const observer = new MutationObserver(findNavbar);
    observer.observe(document.body, { childList: true, subtree: true });
    
    return () => observer.disconnect();
  }, []);

  if (!container) {
    return null;
  }

  // Use React portal to render auth buttons into navbar
  return createPortal(<AuthButtons />, container);
}

function RootContent({ children }: Props) {
  const [showSignUp, setShowSignUp] = useState(false);
  const [showSignIn, setShowSignIn] = useState(false);
  const [showQuestionnaire, setShowQuestionnaire] = useState(false);

  // Listen for openSignUp events from ChatBot
  useEffect(() => {
    const handleOpenSignUp = () => {
      setShowSignUp(true);
    };
    
    const handleOpenSignIn = () => {
      setShowSignIn(true);
    };

    window.addEventListener('openSignUp', handleOpenSignUp);
    window.addEventListener('openSignIn', handleOpenSignIn);
    return () => {
      window.removeEventListener('openSignUp', handleOpenSignUp);
      window.removeEventListener('openSignIn', handleOpenSignIn);
    };
  }, []);

  const handleRegistrationComplete = () => {
    setShowSignUp(false);
    setShowQuestionnaire(true);
  };

  const handleQuestionnaireComplete = () => {
    setShowQuestionnaire(false);
  };

  return (
    <>
      {children}
      <NavbarAuthInjector />
      <ChatBot />
      <SignInModal
        isOpen={showSignIn}
        onClose={() => setShowSignIn(false)}
        onSwitchToSignUp={() => {
          setShowSignIn(false);
          setShowSignUp(true);
        }}
      />
      <SignUpModal
        isOpen={showSignUp}
        onClose={() => setShowSignUp(false)}
        onSwitchToSignIn={() => {
          setShowSignUp(false);
          setShowSignIn(true);
        }}
        onRegistrationComplete={handleRegistrationComplete}
      />
      <Questionnaire
        isOpen={showQuestionnaire}
        onComplete={handleQuestionnaireComplete}
        onSkip={handleQuestionnaireComplete}
      />
    </>
  );
}

export default function Root({ children }: Props): JSX.Element {
  return (
    <AuthProvider>
      <RootContent>{children}</RootContent>
    </AuthProvider>
  );
}
