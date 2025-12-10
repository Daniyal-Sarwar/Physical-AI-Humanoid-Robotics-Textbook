<div align="center">

# 🤖 Physical AI & Humanoid Robotics Textbook

**A comprehensive technical textbook for modern robotics software development**

[![Deploy to GitHub Pages](https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook/actions/workflows/deploy.yml/badge.svg)](https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook/actions/workflows/deploy.yml)
[![Docusaurus](https://img.shields.io/badge/Built%20with-Docusaurus%203-brightgreen?logo=docusaurus)](https://docusaurus.io/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue?logo=typescript)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[📖 **Read the Book**](https://daniyal-sarwar.github.io/Physical-AI-Humanoid-Robotics-Textbook/) · [🐛 Report Bug](https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook/issues) · [✨ Request Feature](https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook/issues)

</div>

---

## 📚 About

This open-source textbook provides a structured 13-week curriculum for learning Physical AI and Humanoid Robotics. Whether you're a student, researcher, or practicing engineer, this guide covers everything from ROS 2 fundamentals to cutting-edge Vision-Language-Action models.

### ✨ Key Features

- 🎓 **Complete Curriculum** — 4 modules, 12 chapters covering the full robotics stack
- 📝 **Hands-On Exercises** — 3 practical exercises per chapter (36 total)
- 💻 **Real Code Examples** — Working Python, C++, and YAML code snippets
- 🧮 **Math Rendering** — Beautiful LaTeX equations with KaTeX
- 📱 **Responsive Design** — Read comfortably on any device
- 🔍 **Full-Text Search** — Find topics instantly
- 🌙 **Dark Mode** — Easy on your eyes during late-night study sessions

---

## 📖 Curriculum Overview

| Module | Duration | Topics |
|--------|----------|--------|
| **🤖 Module 1: ROS 2 Fundamentals** | Weeks 1-3 | Nodes, Topics, Services, Actions, Parameters |
| **🌐 Module 2: Digital Twin Simulation** | Weeks 4-6 | Gazebo Harmonic, URDF/SDF, Unity Robotics Hub |
| **⚡ Module 3: NVIDIA Isaac Platform** | Weeks 7-10 | Isaac Sim, Replicator, Isaac ROS |
| **🧠 Module 4: Vision-Language-Action** | Weeks 11-13 | Voice-to-Action, VLMs, Embodied Agents |

---

## 🚀 Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) v18.x or later
- [npm](https://www.npmjs.com/) or [pnpm](https://pnpm.io/)

### Installation

```bash
# Clone the repository
git clone https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook.git
cd Physical-AI-Humanoid-Robotics-Textbook

# Install dependencies
npm install

# Start development server
npm run start
```

The site will be available at `http://localhost:3000/Physical-AI-Humanoid-Robotics-Textbook/`

### Build for Production

```bash
# Create production build
npm run build

# Preview production build locally
npm run serve
```

---

## 🏗️ Project Structure

```
.
├── docs/                          # 📚 MDX content (chapters)
│   ├── intro.md                   # Book introduction
│   ├── glossary.md                # Robotics terminology
│   ├── notation.md                # Mathematical notation
│   ├── module-1-ros2/             # ROS 2 chapters
│   ├── module-2-simulation/       # Simulation chapters
│   ├── module-3-isaac/            # NVIDIA Isaac chapters
│   └── module-4-vla/              # VLA chapters
├── src/
│   ├── components/                # 🧩 React components
│   │   ├── GlossaryTooltip/       # Hover tooltips for terms
│   │   └── CodeBlock/             # Enhanced code display
│   ├── css/                       # 🎨 Custom styles
│   ├── data/                      # 📊 Glossary data (JSON)
│   └── pages/                     # 📄 Custom pages
├── static/
│   ├── img/                       # 🖼️ Images and diagrams
│   └── examples/                  # 📦 Downloadable code
├── docusaurus.config.ts           # ⚙️ Site configuration
├── sidebars.ts                    # 📑 Navigation structure
└── package.json                   # 📋 Dependencies
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [Docusaurus 3](https://docusaurus.io/) | Static site generator |
| [React 18](https://react.dev/) | UI components |
| [TypeScript](https://www.typescriptlang.org/) | Type-safe development |
| [MDX](https://mdxjs.com/) | Markdown + JSX content |
| [KaTeX](https://katex.org/) | Math equation rendering |
| [Prism](https://prismjs.com/) | Syntax highlighting |
| [GitHub Actions](https://github.com/features/actions) | CI/CD deployment |
| [GitHub Pages](https://pages.github.com/) | Static hosting |

---

## 📝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Content Guidelines

- Each chapter should include learning objectives, prerequisites, and 3 exercises
- Code examples must be tested and working
- Images require descriptive alt text for accessibility
- Use proper heading hierarchy (H2-H4)

---

## 📊 Roadmap

- [x] Core curriculum (4 modules, 12 chapters)
- [x] Interactive glossary tooltips
- [x] Math equation support
- [x] GitHub Pages deployment
- [ ] Lighthouse audit optimization
- [ ] Additional exercises and labs
- [ ] Video walkthroughs
- [ ] Multi-language support

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [NVIDIA Isaac Documentation](https://developer.nvidia.com/isaac-sim)
- [Gazebo Documentation](https://gazebosim.org/)
- [OpenAI Research Papers](https://openai.com/research/)
- [Google DeepMind RT-2](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/)

---

<div align="center">

**[⬆ Back to Top](#-physical-ai--humanoid-robotics-textbook)**

Made with ❤️ for the robotics community

</div>
