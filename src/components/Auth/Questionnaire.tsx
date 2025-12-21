/**
 * Questionnaire Component
 * 
 * Background questionnaire shown after registration to personalize
 * the chatbot experience. Collects:
 * - Programming experience level
 * - Robotics familiarity
 * - Hardware experience
 * - Learning goals
 */

import React, { useState, FormEvent } from 'react';
import { useAuth } from './AuthContext';
import type { ProfileRequest } from '../../services/authService';
import styles from './AuthModals.module.css';

interface QuestionnaireProps {
  isOpen: boolean;
  onComplete: () => void;
  onSkip?: () => void;
}

type Step = 1 | 2 | 3 | 4;

const PROGRAMMING_LEVELS = [
  { value: 'none', label: 'No experience', description: 'New to programming' },
  { value: 'beginner', label: 'Beginner', description: '< 1 year experience' },
  { value: 'intermediate', label: 'Intermediate', description: '1-3 years experience' },
  { value: 'advanced', label: 'Advanced', description: '3+ years experience' },
] as const;

const ROBOTICS_FAMILIARITY = [
  { value: 'none', label: 'No experience', description: 'Never worked with robots' },
  { value: 'hobbyist', label: 'Hobbyist', description: 'Personal projects, makers' },
  { value: 'academic', label: 'Academic', description: 'University courses/research' },
  { value: 'professional', label: 'Professional', description: 'Industry experience' },
] as const;

const HARDWARE_EXPERIENCE = [
  { value: 'none', label: 'No experience', description: 'Software only' },
  { value: 'arduino', label: 'Arduino/Pi', description: 'Maker boards, basic electronics' },
  { value: 'embedded', label: 'Embedded Systems', description: 'Microcontrollers, firmware' },
  { value: 'industrial', label: 'Industrial', description: 'PLCs, industrial automation' },
] as const;

const LEARNING_GOALS = [
  { value: 'career_change', label: 'Career Change', description: 'Transitioning to robotics' },
  { value: 'academic', label: 'Academic', description: 'Research or coursework' },
  { value: 'hobby', label: 'Hobby', description: 'Personal interest, fun projects' },
  { value: 'professional_dev', label: 'Professional Development', description: 'Skill enhancement' },
] as const;

export function Questionnaire({ isOpen, onComplete, onSkip }: QuestionnaireProps) {
  const { createProfile, isLoading, error, clearError } = useAuth();
  const [step, setStep] = useState<Step>(1);
  const [profile, setProfile] = useState<Partial<ProfileRequest>>({});

  if (!isOpen) return null;

  const handleSelect = (field: keyof ProfileRequest, value: string) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (step < 4) {
      setStep((step + 1) as Step);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep((step - 1) as Step);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    clearError();

    try {
      await createProfile(profile as ProfileRequest);
      onComplete();
    } catch (err) {
      // Error handled by AuthContext
    }
  };

  const canProceed = () => {
    switch (step) {
      case 1: return !!profile.programming_level;
      case 2: return !!profile.robotics_familiarity;
      case 3: return !!profile.hardware_experience;
      case 4: return !!profile.learning_goal;
      default: return false;
    }
  };

  const renderOptions = (
    options: readonly { value: string; label: string; description: string }[],
    field: keyof ProfileRequest,
    selected: string | undefined
  ) => (
    <div className={styles.optionsGrid}>
      {options.map(option => (
        <button
          key={option.value}
          type="button"
          className={`${styles.optionCard} ${selected === option.value ? styles.optionSelected : ''}`}
          onClick={() => handleSelect(field, option.value)}
        >
          <span className={styles.optionLabel}>{option.label}</span>
          <span className={styles.optionDescription}>{option.description}</span>
        </button>
      ))}
    </div>
  );

  return (
    <div className={styles.modalOverlay}>
      <div className={`${styles.modalContent} ${styles.questionnaireModal}`}>
        <div className={styles.progressBar}>
          <div 
            className={styles.progressFill} 
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>

        <h2 className={styles.modalTitle}>
          {step === 1 && 'Programming Experience'}
          {step === 2 && 'Robotics Background'}
          {step === 3 && 'Hardware Experience'}
          {step === 4 && 'Learning Goals'}
        </h2>
        
        <p className={styles.modalSubtitle}>
          {step === 1 && 'What is your programming experience level?'}
          {step === 2 && 'How familiar are you with robotics?'}
          {step === 3 && 'What hardware experience do you have?'}
          {step === 4 && 'What brings you to learn Physical AI?'}
        </p>

        {error && (
          <div className={styles.errorMessage}>{error}</div>
        )}

        <form onSubmit={handleSubmit}>
          {step === 1 && renderOptions(PROGRAMMING_LEVELS, 'programming_level', profile.programming_level)}
          {step === 2 && renderOptions(ROBOTICS_FAMILIARITY, 'robotics_familiarity', profile.robotics_familiarity)}
          {step === 3 && renderOptions(HARDWARE_EXPERIENCE, 'hardware_experience', profile.hardware_experience)}
          {step === 4 && renderOptions(LEARNING_GOALS, 'learning_goal', profile.learning_goal)}

          <div className={styles.buttonRow}>
            {step > 1 && (
              <button
                type="button"
                className={styles.secondaryButton}
                onClick={handleBack}
                disabled={isLoading}
              >
                Back
              </button>
            )}
            
            {onSkip && step === 1 && (
              <button
                type="button"
                className={styles.skipButton}
                onClick={onSkip}
              >
                Skip for now
              </button>
            )}

            {step < 4 ? (
              <button
                type="button"
                className={styles.submitButton}
                onClick={handleNext}
                disabled={!canProceed()}
              >
                Continue
              </button>
            ) : (
              <button
                type="submit"
                className={styles.submitButton}
                disabled={!canProceed() || isLoading}
              >
                {isLoading ? 'Saving...' : 'Complete Setup'}
              </button>
            )}
          </div>
        </form>

        <p className={styles.stepIndicator}>
          Step {step} of 4
        </p>
      </div>
    </div>
  );
}

export default Questionnaire;
