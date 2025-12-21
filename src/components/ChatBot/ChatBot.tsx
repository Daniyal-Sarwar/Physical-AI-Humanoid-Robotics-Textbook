/**
 * RAG ChatBot Component
 * 
 * Floating chat widget with Physical AI textbook knowledge.
 * Rate-limited for anonymous users, unlimited for authenticated users.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useAuth } from '../Auth/AuthContext';
import { getRateLimitStatus, generateFingerprint, RateLimitStatus } from '../../services/rateLimitService';
import { RateLimitBanner } from './RateLimitBanner';
import styles from './ChatBot.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const API_URL = 'http://localhost:8000/api/v1';
const isBrowser = typeof window !== 'undefined';

export function ChatBot() {
  const { isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [rateLimitStatus, setRateLimitStatus] = useState<RateLimitStatus | null>(null);
  const [showSignUp, setShowSignUp] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Load rate limit status
  const loadRateLimitStatus = useCallback(async () => {
    if (isAuthenticated) {
      setRateLimitStatus(null);
      return;
    }
    
    try {
      const fingerprint = await generateFingerprint();
      const status = await getRateLimitStatus(fingerprint);
      setRateLimitStatus(status);
    } catch (error) {
      console.error('Failed to load rate limit status:', error);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    loadRateLimitStatus();
  }, [loadRateLimitStatus]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  // Welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{
        id: 'welcome',
        role: 'assistant',
        content: "👋 Hi! I'm your Physical AI learning assistant. Ask me anything about ROS 2, simulation, NVIDIA Isaac, or Vision-Language-Action models!\n\n---\n*Physical AI Textbook™ — Created by [Daniyal Sarwar](https://github.com/Daniyal-Sarwar)*",
        timestamp: new Date()
      }]);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    // Check rate limit for anonymous users
    if (!isAuthenticated && rateLimitStatus && rateLimitStatus.remaining <= 0) {
      setShowSignUp(true);
      return;
    }

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: trimmedInput,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Build request headers
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (!isAuthenticated) {
        const fingerprint = await generateFingerprint();
        headers['X-Fingerprint'] = fingerprint;
      }

      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers,
        credentials: 'include',
        body: JSON.stringify({
          message: trimmedInput,
          context: messages.slice(-6).map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      });

      if (!response.ok) {
        if (response.status === 429) {
          // Rate limited
          await loadRateLimitStatus();
          throw new Error('Rate limit exceeded. Please sign up for unlimited access!');
        }
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response || data.message || "I couldn't process that request.",
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update rate limit status after successful request
      if (!isAuthenticated) {
        await loadRateLimitStatus();
      }
    } catch (error) {
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: error instanceof Error ? error.message : 'Sorry, something went wrong. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleSignUpClick = () => {
    setShowSignUp(true);
    // Dispatch custom event for navbar to open signup modal
    window.dispatchEvent(new CustomEvent('openSignUp'));
  };

  // Only block if explicitly rate limited (remaining === 0)
  const isRateLimited = !isAuthenticated && rateLimitStatus !== null && rateLimitStatus.remaining === 0;
  const canSendMessage = !isLoading && input.trim().length > 0 && !isRateLimited;

  return (
    <>
      {/* Chat Button */}
      <button
        className={`${styles.chatButton} ${isOpen ? styles.chatButtonHidden : ''}`}
        onClick={() => setIsOpen(true)}
        aria-label="Open chat"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path 
            d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0035 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          />
        </svg>
        <span className={styles.chatButtonLabel}>Ask AI</span>
      </button>

      {/* Chat Widget */}
      <div className={`${styles.chatWidget} ${isOpen ? styles.chatWidgetOpen : ''}`}>
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.headerTitle}>
            <span className={styles.headerIcon}>🤖</span>
            <span>Physical AI Assistant</span>
          </div>
          <button 
            className={styles.closeButton}
            onClick={() => setIsOpen(false)}
            aria-label="Close chat"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path 
                d="M13.5 4.5L4.5 13.5M4.5 4.5L13.5 13.5" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round"
              />
            </svg>
          </button>
        </div>

        {/* Rate Limit Banner */}
        {!isAuthenticated && rateLimitStatus && (
          <div className={styles.bannerContainer}>
            <RateLimitBanner 
              status={rateLimitStatus} 
              onSignUpClick={handleSignUpClick}
            />
          </div>
        )}

        {/* Messages */}
        <div className={styles.messages}>
          {messages.map(message => (
            <div
              key={message.id}
              className={`${styles.message} ${
                message.role === 'user' ? styles.userMessage : styles.assistantMessage
              }`}
            >
              {message.role === 'assistant' && (
                <span className={styles.messageIcon}>🤖</span>
              )}
              <div className={styles.messageContent}>
                {message.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className={`${styles.message} ${styles.assistantMessage}`}>
              <span className={styles.messageIcon}>🤖</span>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form className={styles.inputForm} onSubmit={handleSubmit}>
          <textarea
            ref={inputRef}
            className={styles.input}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              !isAuthenticated && rateLimitStatus?.remaining === 0
                ? "Sign up to continue chatting..."
                : "Ask about ROS 2, simulation, Isaac..."
            }
            rows={1}
            disabled={isLoading || isRateLimited}
          />
          <button
            type="submit"
            className={styles.sendButton}
            disabled={!canSendMessage}
            aria-label="Send message"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path 
                d="M18.3333 1.66669L9.16667 10.8334M18.3333 1.66669L12.5 18.3334L9.16667 10.8334M18.3333 1.66669L1.66667 7.50002L9.16667 10.8334" 
                stroke="currentColor" 
                strokeWidth="1.5" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </form>
      </div>
    </>
  );
}

export default ChatBot;
