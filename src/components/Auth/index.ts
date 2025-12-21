/**
 * Auth Components Index
 * 
 * Re-exports all authentication-related components.
 */

export { AuthProvider, useAuth } from './AuthContext';
// Types are exported from authService, not AuthContext
export type { User, UserProfile, UserWithProfile } from '../../services/authService';

export { SignInModal } from './SignInModal';
export { SignUpModal } from './SignUpModal';
export { Questionnaire } from './Questionnaire';
export { AuthButtons } from './AuthButtons';
export { ProfileSettings } from './ProfileSettings';
