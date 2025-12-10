````markdown
# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

## Summary

Build a comprehensive educational textbook on Physical AI and Humanoid Robotics using Docusaurus, deployed as a static site on GitHub Pages. The book covers the complete 13-week course curriculum across 4 modules (ROS 2, Simulation, NVIDIA Isaac, VLA). No backend or chatbot - pure static documentation site.

## Technical Context

**Language/Version**: TypeScript 5.x (Docusaurus)  
**Primary Dependencies**: Docusaurus 3.x, React 18, remark-math, rehype-katex  
**Storage**: Static MDX files (content)  
**Testing**: Jest (components), Playwright (E2E)  
**Target Platform**: GitHub Pages (static site)  
**CI/CD**: GitHub Actions  
**Project Type**: Static documentation site  
**Performance Goals**: Page load <3s, Lighthouse ≥90  
**Constraints**: No backend required, GitHub Pages hosting, Hackathon deadline Nov 30  
**Scale/Scope**: Full 13-week curriculum, 4 modules, all chapters

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status | Notes |
|-----------|------|--------|-------|
| I. Content Accuracy | Code examples tested, citations required | ✅ PASS | Plan includes test coverage for examples |
| II. Educational Clarity | Prerequisites declared, learning objectives stated | ✅ PASS | Chapter template enforces structure |
| III. Consistency | Terminology via glossary, chapter template | ✅ PASS | Will create docs/glossary.md |
| IV. Docusaurus Structure | Metadata required, max 2000 words/page | ✅ PASS | Sidebar organization planned |
| V. Code Example Quality | Complete examples with versions | ✅ PASS | /examples/ structure planned |
| VI. Deployment Standards | Build gates, Lighthouse ≥90 | ✅ PASS | GitHub Actions CI pipeline |

**All gates PASS** - proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
# Docusaurus Book (Frontend)
docs/
├── intro.md                    # Book introduction
├── glossary.md                 # Terminology definitions
├── notation.md                 # Mathematical notation reference
├── module-1-ros2/              # Module 1: ROS 2 Fundamentals
│   ├── _category_.json
│   ├── 01-introduction.mdx
│   ├── 02-nodes-topics.mdx
│   └── ...                     # All curriculum chapters
├── module-2-simulation/        # Module 2: Digital Twin
│   ├── _category_.json
│   ├── 01-gazebo-basics.mdx
│   └── ...                     # All curriculum chapters
├── module-3-isaac/             # Module 3: NVIDIA Isaac
│   ├── _category_.json
│   ├── 01-isaac-sim-intro.mdx
│   └── ...                     # All curriculum chapters
└── module-4-vla/               # Module 4: Vision-Language-Action
    ├── _category_.json
    ├── 01-voice-to-action.mdx
    └── ...                     # All curriculum chapters

src/
├── components/
│   ├── GlossaryTooltip/        # Inline term definitions
│   └── CodeBlock/              # Enhanced code display
├── pages/
│   └── index.tsx               # Landing page
├── css/
│   └── custom.css
└── theme/
    └── Root.tsx                # Theme wrapper

static/
├── img/
│   ├── module-1-ros2/
│   ├── module-2-simulation/
│   ├── module-3-isaac/
│   └── module-4-vla/
└── examples/                   # Downloadable code examples

# Configuration
docusaurus.config.ts            # Docusaurus configuration
sidebars.ts                     # Sidebar navigation
package.json                    # Frontend dependencies

# CI/CD
.github/
└── workflows/
    └── deploy.yml              # GitHub Actions deployment

# Tests
tests/
├── components/
└── e2e/
```

**Structure Decision**: Pure static Docusaurus site deployed to GitHub Pages via GitHub Actions. No backend required.

## Complexity Tracking

No constitution violations requiring justification.

## Deployment Architecture

### GitHub Pages + GitHub Actions

```
Push to main → GitHub Actions → Build Docusaurus → Deploy to gh-pages branch → GitHub Pages serves site
```

**Workflow**: `.github/workflows/deploy.yml`
- Trigger: Push to `main` branch
- Build: `pnpm build`
- Deploy: `peaceiris/actions-gh-pages@v3` or `actions/deploy-pages@v4`
- Output: Static site at `https://<username>.github.io/<repo>/`

### CI Checks (must pass before deploy)
- Docusaurus build succeeds
- Broken link checker passes
- Lighthouse score ≥90

````
