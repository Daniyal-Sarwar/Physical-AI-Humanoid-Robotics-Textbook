/**
 * Rate Limit Service
 * 
 * Handles rate limit status API calls for anonymous users.
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';
const isBrowser = typeof window !== 'undefined';

export interface RateLimitStatus {
  remaining: number;
  total: number;
  reset_at: string;
  is_authenticated: boolean;
}

/**
 * Get current rate limit status
 * 
 * @param fingerprint - Optional browser fingerprint for consistent tracking
 */
export async function getRateLimitStatus(fingerprint?: string): Promise<RateLimitStatus> {
  if (!isBrowser) {
    return { remaining: 3, total: 3, reset_at: new Date().toISOString(), is_authenticated: false };
  }

  const headers: Record<string, string> = {};
  
  if (fingerprint) {
    headers['X-Fingerprint'] = fingerprint;
  }
  
  const response = await fetch(`${API_BASE_URL}/rate-limit/status`, {
    method: 'GET',
    headers,
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Generate a simple browser fingerprint
 * This is a basic implementation - in production, consider using fingerprintjs
 */
export function generateFingerprint(): string {
  if (!isBrowser) {
    return 'ssr-placeholder';
  }

  const components = [
    navigator.userAgent,
    navigator.language,
    screen.width,
    screen.height,
    screen.colorDepth,
    new Date().getTimezoneOffset(),
    navigator.hardwareConcurrency || 'unknown',
  ];
  
  // Simple hash function
  const str = components.join('|');
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  
  return Math.abs(hash).toString(16).padStart(16, '0');
}

/**
 * Format time remaining until rate limit reset
 */
export function formatResetTime(resetAt: string): string {
  const reset = new Date(resetAt);
  const now = new Date();
  const diffMs = reset.getTime() - now.getTime();
  
  if (diffMs <= 0) {
    return 'now';
  }
  
  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  return `${minutes}m`;
}

export default {
  getRateLimitStatus,
  generateFingerprint,
  formatResetTime,
};
