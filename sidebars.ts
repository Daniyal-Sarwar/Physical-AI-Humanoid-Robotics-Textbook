import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

/**
 * Module-based sidebar configuration for Physical AI & Humanoid Robotics Textbook
 * 
 * Structure:
 * - Introduction & Reference (intro, glossary, notation)
 * - Module 1: ROS 2 Fundamentals
 * - Module 2: Digital Twin Simulation
 * - Module 3: NVIDIA Isaac Platform
 * - Module 4: Vision-Language-Action Models
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    // Introduction section
    {
      type: "doc",
      id: "intro",
      label: "Introduction",
    },
    
    // Reference section
    {
      type: "category",
      label: "Reference",
      collapsed: false,
      items: [
        "glossary",
        "notation",
      ],
    },

    // Module 1: ROS 2 Fundamentals
    {
      type: "category",
      label: "Module 1: ROS 2 Fundamentals",
      collapsed: false,
      link: {
        type: "generated-index",
        title: "ROS 2 Fundamentals",
        description: "Learn the foundations of Robot Operating System 2 (ROS 2) for modern robotics development.",
        keywords: ["ros2", "robotics", "middleware"],
      },
      items: [
        "module-1-ros2/introduction",
        "module-1-ros2/nodes-topics",
        "module-1-ros2/actions-parameters",
      ],
    },

    // Module 2: Digital Twin Simulation
    {
      type: "category",
      label: "Module 2: Digital Twin Simulation",
      collapsed: false,
      link: {
        type: "generated-index",
        title: "Digital Twin Simulation",
        description: "Master simulation environments with Gazebo and Unity for robot development and testing.",
        keywords: ["gazebo", "unity", "simulation", "digital-twin"],
      },
      items: [
        "module-2-simulation/gazebo-basics",
        "module-2-simulation/urdf-sdf",
        "module-2-simulation/unity-integration",
      ],
    },

    // Module 3: NVIDIA Isaac Platform
    {
      type: "category",
      label: "Module 3: NVIDIA Isaac Platform",
      collapsed: false,
      link: {
        type: "generated-index",
        title: "NVIDIA Isaac Platform",
        description: "Explore NVIDIA Isaac Sim for high-fidelity simulation and synthetic data generation.",
        keywords: ["isaac-sim", "nvidia", "synthetic-data", "replicator"],
      },
      items: [
        "module-3-isaac/isaac-sim-intro",
        "module-3-isaac/replicator",
        "module-3-isaac/isaac-ros",
      ],
    },

    // Module 4: Vision-Language-Action Models
    {
      type: "category",
      label: "Module 4: Vision-Language-Action",
      collapsed: false,
      link: {
        type: "generated-index",
        title: "Vision-Language-Action Models",
        description: "Understand cutting-edge VLA models that enable robots to understand and act on natural language instructions.",
        keywords: ["vla", "vision-language", "embodied-ai", "multimodal"],
      },
      items: [
        "module-4-vla/voice-to-action",
        "module-4-vla/vision-language-models",
        "module-4-vla/embodied-agents",
      ],
    },
  ],
};

export default sidebars;
