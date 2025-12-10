import React from 'react';
import CodeBlockOriginal from '@theme/CodeBlock';
import styles from './styles.module.css';

interface CodeBlockProps {
  children: string;
  language?: string;
  title?: string;
  showLineNumbers?: boolean;
  metastring?: string;
}

/**
 * Enhanced CodeBlock component with additional features.
 * 
 * Features:
 * - Syntax highlighting for Python, C++, YAML, Bash, JSON
 * - Line numbers (optional)
 * - Title bar with language indicator
 * - Copy button (built into Docusaurus)
 * 
 * Usage in MDX:
 * ```python title="example.py" showLineNumbers
 * import rclpy
 * from rclpy.node import Node
 * ```
 */
export default function CodeBlock({
  children,
  language = 'python',
  title,
  showLineNumbers = false,
  metastring,
}: CodeBlockProps): JSX.Element {
  // Build metastring for Docusaurus CodeBlock
  let meta = metastring || '';
  if (showLineNumbers && !meta.includes('showLineNumbers')) {
    meta = `${meta} showLineNumbers`.trim();
  }

  return (
    <div className={styles.codeBlockWrapper}>
      {title && (
        <div className={styles.codeBlockTitle}>
          <span className={styles.languageBadge}>{language.toUpperCase()}</span>
          <span className={styles.titleText}>{title}</span>
        </div>
      )}
      <CodeBlockOriginal
        language={language}
        title={!title ? undefined : undefined} // Use custom title above
        metastring={meta}
      >
        {children}
      </CodeBlockOriginal>
    </div>
  );
}
