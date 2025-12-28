---
sidebar_position: 3
title: Mathematical Notation
description: Mathematical notation and conventions used throughout the textbook
---

# Mathematical Notation

> Reference guide for mathematical symbols and conventions used in this textbook.

## General Conventions

| Symbol | Meaning | Example |
|--------|---------|---------|
| $x$ | Scalar (lowercase italic) | Position $x = 5.0$ |
| $\mathbf{x}$ | Vector (bold lowercase) | Position vector $\mathbf{x} = [x, y, z]^T$ |
| $\mathbf{X}$ | Matrix (bold uppercase) | Rotation matrix $\mathbf{R}$ |
| $\hat{\mathbf{x}}$ | Unit vector | Unit direction $\hat{\mathbf{x}}$ |
| $\dot{x}$ | Time derivative | Velocity $\dot{x} = \frac{dx}{dt}$ |
| $\ddot{x}$ | Second time derivative | Acceleration $\ddot{x} = \frac{d^2x}{dt^2}$ |

---

## Coordinate Frames

### Frame Notation

We use superscripts and subscripts to denote coordinate frames:

- ${}^A\mathbf{p}_B$ — Position of point $B$ expressed in frame $A$
- ${}^A\mathbf{R}_B$ — Rotation matrix from frame $B$ to frame $A$
- ${}^A\mathbf{T}_B$ — Homogeneous transformation from frame $B$ to frame $A$

### Common Frames

| Frame | Description |
|-------|-------------|
| $W$ or $O$ | World/Origin frame (fixed, inertial) |
| $B$ | Robot base frame |
| $E$ | End-effector frame |
| $C$ | Camera frame |
| $S$ | Sensor frame |

---

## Transformations

### Rotation Matrix

A $3 \times 3$ orthonormal matrix $\mathbf{R} \in SO(3)$ representing orientation:

$$
\mathbf{R} = \begin{bmatrix} 
r_{11} & r_{12} & r_{13} \\
r_{21} & r_{22} & r_{23} \\
r_{31} & r_{32} & r_{33}
\end{bmatrix}
$$

**Properties:**
- $\mathbf{R}^T \mathbf{R} = \mathbf{I}$
- $\det(\mathbf{R}) = 1$
- $\mathbf{R}^{-1} = \mathbf{R}^T$

### Euler Angles

Roll ($\phi$), Pitch ($\theta$), Yaw ($\psi$) — intrinsic ZYX convention:

$$
\mathbf{R} = \mathbf{R}_z(\psi) \mathbf{R}_y(\theta) \mathbf{R}_x(\phi)
$$

### Quaternion

Unit quaternion $\mathbf{q} = [q_w, q_x, q_y, q_z]$ where:

$$
\|\mathbf{q}\| = \sqrt{q_w^2 + q_x^2 + q_y^2 + q_z^2} = 1
$$

### Homogeneous Transformation

A $4 \times 4$ matrix combining rotation and translation:

$$
\mathbf{T} = \begin{bmatrix} 
\mathbf{R} & \mathbf{t} \\
\mathbf{0}^T & 1
\end{bmatrix} = \begin{bmatrix} 
r_{11} & r_{12} & r_{13} & t_x \\
r_{21} & r_{22} & r_{23} & t_y \\
r_{31} & r_{32} & r_{33} & t_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

---

## Kinematics

### Joint Variables

- $\mathbf{q} = [q_1, q_2, \ldots, q_n]^T$ — Joint positions
- $\dot{\mathbf{q}}$ — Joint velocities
- $\ddot{\mathbf{q}}$ — Joint accelerations
- $\boldsymbol{\tau}$ — Joint torques

### Forward Kinematics

$$
\mathbf{x} = f(\mathbf{q})
$$

Where $\mathbf{x}$ is end-effector pose and $\mathbf{q}$ is joint configuration.

### Jacobian

The Jacobian $\mathbf{J}(\mathbf{q})$ relates joint velocities to end-effector velocities:

$$
\dot{\mathbf{x}} = \mathbf{J}(\mathbf{q}) \dot{\mathbf{q}}
$$

### Inverse Kinematics

$$
\mathbf{q} = f^{-1}(\mathbf{x})
$$

Often solved numerically using:
$$
\dot{\mathbf{q}} = \mathbf{J}^{\dagger}(\mathbf{q}) \dot{\mathbf{x}}
$$

Where $\mathbf{J}^{\dagger}$ is the pseudoinverse.

---

## Dynamics

### Equation of Motion

$$
\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) = \boldsymbol{\tau}
$$

Where:
- $\mathbf{M}(\mathbf{q})$ — Mass/inertia matrix
- $\mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})$ — Coriolis and centrifugal terms
- $\mathbf{g}(\mathbf{q})$ — Gravity vector
- $\boldsymbol{\tau}$ — Applied joint torques

---

## Probability & Statistics

### Probability

| Symbol | Meaning |
|--------|---------|
| $P(A)$ | Probability of event $A$ |
| $P(A \mid B)$ | Conditional probability of $A$ given $B$ |
| $\mathbb{E}[X]$ | Expected value of $X$ |
| $\text{Var}(X)$ | Variance of $X$ |
| $\mathcal{N}(\mu, \sigma^2)$ | Normal distribution with mean $\mu$ and variance $\sigma^2$ |

### Gaussian Distribution

$$
p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

Multivariate:
$$
p(\mathbf{x}) = \frac{1}{(2\pi)^{n/2}|\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right)
$$

---

## Control Theory

### State-Space Representation

$$
\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}
$$
$$
\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}
$$

Where:
- $\mathbf{x}$ — State vector
- $\mathbf{u}$ — Control input
- $\mathbf{y}$ — Output
- $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$ — System matrices

### PID Control

$$
u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}
$$

Where $e(t) = r(t) - y(t)$ is the error between reference $r$ and output $y$.

---

## Machine Learning

### Loss Function

$$
\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f_\theta(x_i), y_i)
$$

### Gradient Descent

$$
\theta_{t+1} = \theta_t - \alpha \nabla_\theta \mathcal{L}(\theta_t)
$$

Where $\alpha$ is the learning rate.

### Policy Gradient

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \nabla_\theta \log \pi_\theta(a|s) \cdot R \right]
$$

---

## Units

Unless otherwise specified:

| Quantity | SI Unit | Symbol |
|----------|---------|--------|
| Length | meter | m |
| Mass | kilogram | kg |
| Time | second | s |
| Angle | radian | rad |
| Force | newton | N |
| Torque | newton-meter | N·m |
| Velocity | m/s | m/s |
| Angular velocity | rad/s | rad/s |
