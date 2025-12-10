# Module 3: Isaac Examples

This directory contains downloadable code examples for Module 3: NVIDIA Isaac Platform.

## Contents

- `isaac_sim_basic.py` - Basic Isaac Sim scene setup
- `replicator_example.py` - Synthetic data generation with Replicator
- `isaac_ros_bridge.py` - Isaac ROS integration example

## Prerequisites

- NVIDIA Isaac Sim 2023.1.1 or later
- NVIDIA GPU with RTX support
- ROS 2 Humble (for ROS integration)

## Usage

```bash
# Launch Isaac Sim with the script
./python.sh isaac_sim_basic.py

# For Replicator example
./python.sh replicator_example.py --output-dir /tmp/synthetic_data
```

## Notes

These examples should be run from within the Isaac Sim environment using
the bundled Python interpreter (`./python.sh`).
