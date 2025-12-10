# Module 2: Simulation Examples

This directory contains downloadable code examples for Module 2: Digital Twin Simulation.

## Contents

- `simple_robot.urdf` - Basic robot URDF description
- `gazebo_world.sdf` - Simple Gazebo world file
- `spawn_robot.py` - Script to spawn robot in Gazebo

## Prerequisites

- ROS 2 Humble or later
- Gazebo Harmonic
- ros_gz packages

## Usage

```bash
# Launch Gazebo with the world
gz sim gazebo_world.sdf

# In another terminal, spawn the robot
python3 spawn_robot.py
```
