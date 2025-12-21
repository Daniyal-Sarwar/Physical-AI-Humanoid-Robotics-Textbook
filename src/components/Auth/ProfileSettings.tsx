/**
 * Profile Settings Component
 * 
 * Allows authenticated users to edit their background questionnaire answers.
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { ProfileRequest } from '../../services/authService';
import styles from './AuthModals.module.css';

interface ProfileSettingsProps {
  isOpen: boolean;
  onClose: () => void;
}

// Type aliases for literal types
type ProgrammingLevel = ProfileRequest['programming_level'];
type RoboticsFamiliarity = ProfileRequest['robotics_familiarity'];
type HardwareExperience = ProfileRequest['hardware_experience'];
type LearningGoal = ProfileRequest['learning_goal'];

const PROGRAMMING_LEVELS: { value: ProgrammingLevel; label: string; description: string }[] = [
  { value: 'none', label: 'None', description: 'New to programming' },
  { value: 'beginner', label: 'Beginner', description: 'Learning basics' },
  { value: 'intermediate', label: 'Intermediate', description: '1-3 years experience' },
  { value: 'advanced', label: 'Advanced', description: '3+ years experience' },
];

const ROBOTICS_FAMILIARITY: { value: RoboticsFamiliarity; label: string; description: string }[] = [
  { value: 'none', label: 'None', description: 'Never worked with robots' },
  { value: 'hobbyist', label: 'Hobbyist', description: 'Personal projects only' },
  { value: 'academic', label: 'Academic', description: 'University/research' },
  { value: 'professional', label: 'Professional', description: 'Industry experience' },
];

const HARDWARE_EXPERIENCE: { value: HardwareExperience; label: string; description: string }[] = [
  { value: 'none', label: 'None', description: 'Software only' },
  { value: 'arduino', label: 'Arduino/Basic', description: 'Arduino, Raspberry Pi' },
  { value: 'embedded', label: 'Embedded', description: 'Sensors, actuators' },
  { value: 'industrial', label: 'Industrial', description: 'Full robot systems' },
];

const LEARNING_GOALS: { value: LearningGoal; label: string; description: string }[] = [
  { value: 'career_change', label: 'Career Change', description: 'Transition to robotics' },
  { value: 'professional_dev', label: 'Professional Dev', description: 'Add to existing skills' },
  { value: 'academic', label: 'Academic', description: 'Research projects' },
  { value: 'hobby', label: 'Hobby', description: 'Personal interest' },
];

export function ProfileSettings({ isOpen, onClose }: ProfileSettingsProps) {
  const { user, updateProfile, refreshUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  // Individual state for each field to maintain proper types
  const [programmingLevel, setProgrammingLevel] = useState<'none' | 'beginner' | 'intermediate' | 'advanced'>('none');
  const [roboticsFamiliarity, setRoboticsFamiliarity] = useState<'none' | 'hobbyist' | 'academic' | 'professional'>('none');
  const [hardwareExperience, setHardwareExperience] = useState<'none' | 'arduino' | 'embedded' | 'industrial'>('none');
  const [learningGoal, setLearningGoal] = useState<'career_change' | 'academic' | 'hobby' | 'professional_dev'>('hobby');

  // Initialize form with user's current profile
  useEffect(() => {
    if (user?.profile) {
      setProgrammingLevel((user.profile.programming_level as ProgrammingLevel) || 'none');
      setRoboticsFamiliarity((user.profile.robotics_familiarity as RoboticsFamiliarity) || 'none');
      setHardwareExperience((user.profile.hardware_experience as HardwareExperience) || 'none');
      setLearningGoal((user.profile.learning_goal as LearningGoal) || 'hobby');
    }
  }, [user?.profile, isOpen]);

  // Reset states when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setError(null);
      setSuccess(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const clearMessages = () => {
    setError(null);
    setSuccess(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setIsLoading(true);
    setError(null);

    try {
      await updateProfile({
        programming_level: programmingLevel as ProfileRequest['programming_level'],
        robotics_familiarity: roboticsFamiliarity as ProfileRequest['robotics_familiarity'],
        hardware_experience: hardwareExperience as ProfileRequest['hardware_experience'],
        learning_goal: learningGoal as ProfileRequest['learning_goal'],
      });
      await refreshUser();
      setSuccess(true);
      
      // Close after short delay to show success
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modal} onClick={e => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitle}>Edit Profile</h2>
          <button className={styles.closeButton} onClick={onClose} aria-label="Close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit} className={styles.modalBody}>
          <p className={styles.subtitle}>
            Update your background to get personalized learning recommendations.
          </p>

          {error && (
            <div className={styles.error}>{error}</div>
          )}

          {success && (
            <div className={styles.success}>
              ✓ Profile updated successfully!
            </div>
          )}

          <div className={styles.profileSections}>
            {/* Programming Level */}
            <div className={styles.questionGroup}>
              <label className={styles.questionLabel}>Programming Level</label>
              <div className={styles.optionsGrid}>
                {PROGRAMMING_LEVELS.map(option => (
                  <button
                    key={option.value}
                    type="button"
                    className={`${styles.optionCard} ${programmingLevel === option.value ? styles.optionSelected : ''}`}
                    onClick={() => { setProgrammingLevel(option.value); clearMessages(); }}
                  >
                    <span className={styles.optionLabel}>{option.label}</span>
                    <span className={styles.optionDescription}>{option.description}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Robotics Familiarity */}
            <div className={styles.questionGroup}>
              <label className={styles.questionLabel}>Robotics Familiarity</label>
              <div className={styles.optionsGrid}>
                {ROBOTICS_FAMILIARITY.map(option => (
                  <button
                    key={option.value}
                    type="button"
                    className={`${styles.optionCard} ${roboticsFamiliarity === option.value ? styles.optionSelected : ''}`}
                    onClick={() => { setRoboticsFamiliarity(option.value); clearMessages(); }}
                  >
                    <span className={styles.optionLabel}>{option.label}</span>
                    <span className={styles.optionDescription}>{option.description}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Hardware Experience */}
            <div className={styles.questionGroup}>
              <label className={styles.questionLabel}>Hardware Experience</label>
              <div className={styles.optionsGrid}>
                {HARDWARE_EXPERIENCE.map(option => (
                  <button
                    key={option.value}
                    type="button"
                    className={`${styles.optionCard} ${hardwareExperience === option.value ? styles.optionSelected : ''}`}
                    onClick={() => { setHardwareExperience(option.value); clearMessages(); }}
                  >
                    <span className={styles.optionLabel}>{option.label}</span>
                    <span className={styles.optionDescription}>{option.description}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Learning Goal */}
            <div className={styles.questionGroup}>
              <label className={styles.questionLabel}>Learning Goal</label>
              <div className={styles.optionsGrid}>
                {LEARNING_GOALS.map(option => (
                  <button
                    key={option.value}
                    type="button"
                    className={`${styles.optionCard} ${learningGoal === option.value ? styles.optionSelected : ''}`}
                    onClick={() => { setLearningGoal(option.value); clearMessages(); }}
                  >
                    <span className={styles.optionLabel}>{option.label}</span>
                    <span className={styles.optionDescription}>{option.description}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className={styles.modalFooter}>
            <button 
              type="button" 
              className={styles.secondaryButton}
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className={styles.primaryButton}
              disabled={isLoading}
            >
              {isLoading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ProfileSettings;
