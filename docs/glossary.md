---
sidebar_position: 2
title: Glossary
description: Key terminology and definitions for Physical AI and robotics
---

# Glossary

> Essential terminology for Physical AI and robotics software development.

## Core Concepts

### ROS 2
**Robot Operating System 2** - A set of software libraries and tools for building robot applications. ROS 2 provides hardware abstraction, device drivers, communication middleware, and common functionality. Unlike its predecessor, ROS 2 is built on the DDS standard for real-time communication.

### Digital Twin
A virtual representation of a physical robot or system that mirrors its real-world counterpart. Digital twins are used for simulation, testing, monitoring, and predictive maintenance.

### Physical AI
Artificial intelligence systems designed to operate in and interact with the physical world, typically through robotic embodiment. Physical AI combines perception, reasoning, planning, and action.

---

## ROS 2 Concepts

### Node
A process that performs computation in ROS 2. Nodes communicate with each other using topics, services, and actions. Each node should be responsible for a single, modular purpose.

### Topic
A named bus over which nodes exchange messages in a publish-subscribe pattern. Topics are used for continuous data streams like sensor readings or robot state.

### Service
A request-reply communication pattern in ROS 2. Services are used when you need a synchronous response to a request, such as spawning an object or getting a transformation.

### Action
A communication pattern for long-running tasks that provides feedback during execution and can be cancelled. Actions are ideal for tasks like navigation or manipulation.

### Parameter
A named configuration value that can be set at node startup or changed dynamically at runtime. Parameters allow tuning of node behavior without recompilation.

### DDS
**Data Distribution Service** - The communication middleware standard used by ROS 2 for reliable, real-time data exchange between nodes. Common implementations include Fast DDS and Cyclone DDS.

### QoS (Quality of Service)
Policies in ROS 2 that control the reliability, durability, and timing of message delivery. QoS profiles allow optimization for different use cases (reliable vs. best-effort).

### TF2
The transform library in ROS 2 that tracks coordinate frames over time. TF2 enables transformation of data (like sensor readings) between different reference frames (like robot base to camera).

---

## Simulation

### URDF
**Unified Robot Description Format** - An XML format for representing a robot model, including links (rigid bodies), joints (connections), and visual/collision geometry.

### SDF
**Simulation Description Format** - An XML format that describes objects and environments for robot simulators. SDF extends URDF with additional simulation-specific features.

### Gazebo
An open-source 3D robotics simulator that integrates with ROS 2. Gazebo provides physics simulation, sensor simulation, and visualization for robot development and testing.

### Physics Engine
Software that simulates physical interactions like collisions, gravity, and friction. Common engines include ODE, Bullet, and NVIDIA PhysX.

---

## NVIDIA Isaac

### Isaac Sim
NVIDIA's robotics simulation platform built on Omniverse. Isaac Sim offers photorealistic rendering, accurate physics, and tools for synthetic data generation.

### Replicator
NVIDIA's synthetic data generation tool. Replicator creates labeled training data for computer vision and machine learning by randomizing scenes, objects, and lighting.

### Isaac ROS
NVIDIA's hardware-accelerated ROS 2 packages optimized for Jetson and GPU platforms. Isaac ROS provides high-performance implementations of common robotics algorithms.

### Omniverse
NVIDIA's platform for creating and operating 3D virtual worlds. Omniverse uses USD (Universal Scene Description) as its foundation.

---

## AI & Machine Learning

### VLA (Vision-Language-Action)
A class of AI models that combine visual perception, natural language understanding, and action generation. VLA models enable robots to follow natural language instructions.

### VLM (Vision-Language Model)
An AI model that can understand and reason about both images and text. VLMs are used for scene understanding, object recognition, and visual question answering.

### Embodied AI
AI systems that interact with the physical world through a robotic body. Embodied AI emphasizes the importance of physical interaction for learning and intelligence.

### Imitation Learning
A machine learning approach where a robot learns to perform tasks by observing and mimicking expert demonstrations. Also known as "learning from demonstration."

### Reinforcement Learning (RL)
A machine learning paradigm where an agent learns to make decisions by receiving rewards or penalties for actions taken in an environment.

### Policy
In reinforcement learning, a policy is a mapping from states to actions that defines the agent's behavior. Policies can be deterministic or stochastic.

---

## Perception

### Point Cloud
A set of 3D points representing the external surface of objects, typically captured by LiDAR or depth cameras. Point clouds are used for 3D mapping and object detection.

### SLAM
**Simultaneous Localization and Mapping** - Algorithms that allow a robot to build a map of an unknown environment while simultaneously tracking its location within that map.

### Object Detection
Computer vision task of identifying and localizing objects in images or point clouds. Common approaches include YOLO, Faster R-CNN, and PointPillars.

### Semantic Segmentation
Assigning a class label to every pixel in an image. Used for understanding scene structure and identifying traversable areas.

---

## Motion & Control

### Kinematics
The study of motion without considering forces. Forward kinematics calculates end-effector position from joint angles; inverse kinematics calculates joint angles from desired position.

### Dynamics
The study of forces and torques required to produce motion. Robot dynamics are essential for trajectory optimization and force control.

### PID Controller
**Proportional-Integral-Derivative Controller** - A feedback control algorithm that calculates an error value and applies corrections based on proportional, integral, and derivative terms.

### Motion Planning
Algorithms that compute collision-free paths for robots to move from start to goal configurations. Common planners include RRT, PRM, and optimization-based methods.

### Trajectory
A time-parameterized path that specifies position, velocity, and sometimes acceleration at each time step. Trajectories are used for smooth robot motion.
