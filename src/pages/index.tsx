import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import styles from './index.module.css';

interface ModuleCardProps {
  title: string;
  weeks: string;
  description: string;
  link: string;
  icon: string;
}

function ModuleCard({ title, weeks, description, link, icon }: ModuleCardProps) {
  const url = useBaseUrl(link);
  return (
    <div className={styles.moduleCard}>
      <div className={styles.moduleIcon}>{icon}</div>
      <div className={styles.moduleContent}>
        <h3 className={styles.moduleTitle}>{title}</h3>
        <span className={styles.moduleWeeks}>{weeks}</span>
        <p className={styles.moduleDescription}>{description}</p>
        <Link className={styles.moduleLink} to={url}>
          Start Learning →
        </Link>
      </div>
    </div>
  );
}

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const introUrl = useBaseUrl('/intro');
  const moduleUrl = useBaseUrl('/module-1-ros2/introduction');
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <div className={styles.heroButtons}>
          <Link
            className={clsx('button button--secondary button--lg', styles.heroButton)}
            to={introUrl}
          >
            Start Reading
          </Link>
          <Link
            className={clsx('button button--outline button--lg', styles.heroButtonOutline)}
            to={moduleUrl}
          >
            Jump to Module 1
          </Link>
        </div>
      </div>
    </header>
  );
}

const modules: ModuleCardProps[] = [
  {
    title: 'Module 1: ROS 2 Fundamentals',
    weeks: 'Weeks 1-3',
    description:
      'Master Robot Operating System 2 architecture, nodes, topics, services, and actions for humanoid robot development.',
    link: '/module-1-ros2/introduction',
    icon: '🤖',
  },
  {
    title: 'Module 2: Digital Twin Simulation',
    weeks: 'Weeks 4-6',
    description:
      'Build high-fidelity digital twins using Gazebo Harmonic, URDF/SDF, and Unity for physics-based robot simulation.',
    link: '/module-2-simulation/gazebo-basics',
    icon: '🌐',
  },
  {
    title: 'Module 3: NVIDIA Isaac Platform',
    weeks: 'Weeks 7-10',
    description:
      'Leverage Isaac Sim for photorealistic simulation, synthetic data generation, and GPU-accelerated perception.',
    link: '/module-3-isaac/isaac-sim-intro',
    icon: '⚡',
  },
  {
    title: 'Module 4: Vision-Language-Action',
    weeks: 'Weeks 11-13',
    description:
      'Deploy cutting-edge VLA models for natural language robot control and end-to-end embodied intelligence.',
    link: '/module-4-vla/voice-to-action',
    icon: '🧠',
  },
];

function ModulesSection() {
  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Curriculum Overview</h2>
        <p className={styles.sectionSubtitle}>
          A comprehensive 13-week journey from ROS 2 fundamentals to advanced embodied AI
        </p>
        <div className={styles.modulesGrid}>
          {modules.map((module, idx) => (
            <ModuleCard key={idx} {...module} />
          ))}
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📚</div>
            <h3>Hands-On Learning</h3>
            <p>
              Every chapter includes practical exercises with real code examples in Python and C++.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🔬</div>
            <h3>Research-Grade Content</h3>
            <p>
              Curriculum designed around state-of-the-art papers from robotics and embodied AI.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🎯</div>
            <h3>Industry-Ready Skills</h3>
            <p>
              Learn the exact tools and frameworks used at NVIDIA, Boston Dynamics, and leading labs.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): React.JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive textbook for Physical AI and Humanoid Robotics"
    >
      <HomepageHeader />
      <main>
        <ModulesSection />
        <FeaturesSection />
      </main>
    </Layout>
  );
}
