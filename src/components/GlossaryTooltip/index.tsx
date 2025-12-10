import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

interface GlossaryTooltipProps {
  term: string;
  definition: string;
  children: React.ReactNode;
}

/**
 * GlossaryTooltip component displays term definitions on hover/click.
 * 
 * Usage in MDX:
 * ```mdx
 * <GlossaryTooltip term="ROS 2" definition="Robot Operating System 2, a set of software libraries and tools for building robot applications.">
 *   ROS 2
 * </GlossaryTooltip>
 * ```
 */
export default function GlossaryTooltip({ 
  term, 
  definition, 
  children 
}: GlossaryTooltipProps): JSX.Element {
  const [isVisible, setIsVisible] = useState(false);
  const tooltipRef = useRef<HTMLSpanElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  // Position tooltip to avoid overflow
  useEffect(() => {
    if (isVisible && tooltipRef.current && contentRef.current) {
      const tooltip = tooltipRef.current;
      const content = contentRef.current;
      const rect = tooltip.getBoundingClientRect();
      const contentRect = content.getBoundingClientRect();
      
      // Adjust horizontal position if overflowing
      if (rect.left + contentRect.width / 2 > window.innerWidth) {
        content.style.left = 'auto';
        content.style.right = '0';
        content.style.transform = 'none';
      } else if (rect.left - contentRect.width / 2 < 0) {
        content.style.left = '0';
        content.style.right = 'auto';
        content.style.transform = 'none';
      }
    }
  }, [isVisible]);

  return (
    <span
      ref={tooltipRef}
      className={styles.glossaryTooltip}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onClick={() => setIsVisible(!isVisible)}
      role="button"
      tabIndex={0}
      aria-label={`${term}: ${definition}`}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          setIsVisible(!isVisible);
        }
      }}
    >
      {children}
      {isVisible && (
        <div 
          ref={contentRef}
          className={styles.tooltipContent}
          role="tooltip"
        >
          <strong className={styles.tooltipTerm}>{term}</strong>
          <p className={styles.tooltipDefinition}>{definition}</p>
        </div>
      )}
    </span>
  );
}
