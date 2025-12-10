````markdown
# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/001-physical-ai-textbook/`  
**Prerequisites**: plan.md ✅, spec.md ✅

**Tests**: Tests are OPTIONAL for this project. Integration validation via quickstart.md workflow.

**Organization**: Tasks grouped by phase for sequential implementation of static book site.

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- All paths are absolute from repository root

## Path Conventions (from plan.md)

```text
docs/                  # MDX content (chapters)
src/components/        # React components
src/pages/             # Custom pages
.github/workflows/     # GitHub Actions CI/CD
```

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Docusaurus project with GitHub Pages deployment

- [x] T001 Initialize Docusaurus 3.x project with TypeScript in repository root
- [x] T002 [P] Configure docusaurus.config.ts with docs route as homepage, MDX support, math rendering (remark-math, rehype-katex)
- [x] T003 [P] Create sidebars.ts with module-based navigation structure
- [x] T004 [P] Create package.json scripts for dev, build, serve
- [x] T005 [P] Create .github/workflows/deploy.yml for GitHub Actions deployment to GitHub Pages
- [x] T006 [P] Create .gitignore for node_modules, build/, .docusaurus/
- [ ] T007 [P] Configure GitHub repository settings for Pages deployment (gh-pages branch or Actions)

**Checkpoint**: Project skeleton ready - site builds and deploys to GitHub Pages

---

## Phase 2: Foundational (Core Infrastructure)

**Purpose**: Base theme, components, and content structure

- [x] T008 Create src/css/custom.css with base theme variables and typography
- [x] T009 [P] Create src/theme/Root.tsx wrapper component if needed for providers (SKIPPED - not needed)
- [x] T010 [P] Create src/components/GlossaryTooltip/index.tsx with hover/click term definitions
- [x] T011 [P] Create src/components/CodeBlock/index.tsx with syntax highlighting for Python, C++, YAML
- [x] T012 [P] Create src/data/glossary.json with initial glossary terms structure
- [x] T013 [P] Create docs/glossary.md with robotics terminology (links to glossary.json)
- [x] T014 [P] Create docs/notation.md with mathematical notation reference
- [x] T015 Create docs/intro.md with book introduction and navigation guide

**Checkpoint**: Foundation ready - site has styling, components, and reference pages

---

## Phase 3: Content - Module 1 (ROS 2 Fundamentals)

**Goal**: Complete all chapters for Module 1 covering ROS 2 basics

- [x] T016 [P] Create docs/module-1-ros2/_category_.json with module metadata
- [x] T017 Create docs/module-1-ros2/01-introduction.mdx with learning objectives, prerequisites, content, 3 exercises, references
- [x] T018 [P] Create docs/module-1-ros2/02-nodes-topics.mdx (Nodes, Topics, Services)
- [x] T019 [P] Create docs/module-1-ros2/03-actions-parameters.mdx (Actions, Parameters)
- [x] T020 [P] Create static/img/module-1-ros2/ with diagrams and images (directory created)
- [x] T021 [P] Create static/examples/module-1-ros2/ with downloadable code examples

**Checkpoint**: Module 1 complete with all chapters, images, and examples

---

## Phase 4: Content - Module 2 (Digital Twin Simulation)

**Goal**: Complete all chapters for Module 2 covering Gazebo/Unity simulation

- [x] T022 [P] Create docs/module-2-simulation/_category_.json with module metadata
- [x] T023 Create docs/module-2-simulation/01-gazebo-basics.mdx with learning objectives, prerequisites, content, 3 exercises, references
- [x] T024 [P] Create docs/module-2-simulation/02-urdf-sdf.mdx (Robot Description Formats)
- [x] T025 [P] Create docs/module-2-simulation/03-unity-integration.mdx (Unity Robotics Hub)
- [x] T026 [P] Create static/img/module-2-simulation/ with diagrams and images (directory created)
- [x] T027 [P] Create static/examples/module-2-simulation/ with downloadable code examples

**Checkpoint**: Module 2 complete with all chapters, images, and examples

---

## Phase 5: Content - Module 3 (NVIDIA Isaac Platform)

**Goal**: Complete all chapters for Module 3 covering NVIDIA Isaac Sim/SDK

- [x] T028 [P] Create docs/module-3-isaac/_category_.json with module metadata
- [x] T029 Create docs/module-3-isaac/01-isaac-sim-intro.mdx with learning objectives, prerequisites, content, 3 exercises, references
- [x] T030 [P] Create docs/module-3-isaac/02-replicator.mdx (Synthetic Data Generation)
- [x] T031 [P] Create docs/module-3-isaac/03-isaac-ros.mdx (Isaac ROS Integration)
- [x] T032 [P] Create static/img/module-3-isaac/ with diagrams and images (directory created)
- [x] T033 [P] Create static/examples/module-3-isaac/ with downloadable code examples

**Checkpoint**: Module 3 complete with all chapters, images, and examples

---

## Phase 6: Content - Module 4 (Vision-Language-Action)

**Goal**: Complete all chapters for Module 4 covering VLA models

- [x] T034 [P] Create docs/module-4-vla/_category_.json with module metadata
- [x] T035 Create docs/module-4-vla/01-voice-to-action.mdx with learning objectives, prerequisites, content, 3 exercises, references
- [x] T036 [P] Create docs/module-4-vla/02-vision-language-models.mdx (VLMs for Robotics)
- [x] T037 [P] Create docs/module-4-vla/03-embodied-agents.mdx (Embodied AI Agents)
- [x] T038 [P] Create static/img/module-4-vla/ with diagrams and images (directory created)
- [x] T039 [P] Create static/examples/module-4-vla/ with downloadable code examples

**Checkpoint**: Module 4 complete with all chapters, images, and examples

---

## Phase 7: Polish & Deployment

**Purpose**: Final validation, CI checks, and production deployment

- [x] T040 Create src/pages/index.tsx landing page with module cards and navigation
- [x] T041 [P] Update docs/intro.md with complete table of contents
- [x] T042 Validate all MDX files render without errors (npm build) ✅ BUILD PASSES
- [x] T043 Run broken link checker and fix any issues ✅ NO BROKEN LINKS
- [ ] T044 Run Lighthouse audit and verify scores ≥90 (accessibility, performance)
- [ ] T045 Verify GitHub Actions deploys successfully to GitHub Pages
- [ ] T046 Test site on mobile and desktop browsers
- [ ] T047 Run quickstart.md validation checklist end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3-6 (Content Modules) ← Can run in parallel
    ↓
Phase 7 (Polish)
```

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup
- **Content Modules (Phase 3-6)**: Depend on Foundational; can run in parallel with each other
- **Polish (Phase 7)**: Depends on all content modules complete

### Parallel Opportunities

**Phase 1 (after T001)**:
```bash
T002 & T003 & T004 & T005 & T006 & T007  # All parallel
```

**Phase 2 (parallel groups)**:
```bash
T009 & T010 & T011 & T012 & T013 & T014  # All parallel
T008 → T015  # Sequential (CSS then intro)
```

**Phase 3-6 (all modules parallel)**:
```bash
# All modules can be developed in parallel:
Phase 3 (Module 1) | Phase 4 (Module 2) | Phase 5 (Module 3) | Phase 6 (Module 4)
```

---

## Summary

| Phase | Task Count | Parallel Tasks | Description |
|-------|-----------|----------------|-------------|
| 1. Setup | 7 | 6 | Project initialization + GitHub Actions |
| 2. Foundational | 8 | 6 | Components, glossary, notation |
| 3. Module 1 (ROS 2) | 6 | 4 | ROS 2 Fundamentals chapters |
| 4. Module 2 (Simulation) | 6 | 4 | Gazebo/Unity chapters |
| 5. Module 3 (Isaac) | 6 | 4 | NVIDIA Isaac chapters |
| 6. Module 4 (VLA) | 6 | 4 | Vision-Language-Action chapters |
| 7. Polish | 8 | 1 | Validation and deployment |
| **Total** | **47** | **29** | |

**Key Changes from Previous Version**:
- ❌ Removed: Phase 4 (RAG Chatbot) - 15 tasks eliminated
- ❌ Removed: Backend API tasks (FastAPI, Qdrant, OpenAI)
- ✅ Added: GitHub Actions deployment (T005, T007, T045)
- ✅ Added: Math rendering configuration (T002 updated)
- ✅ Changed: Scope from representative chapters to full curriculum

**Success Criteria Coverage**:
- SC-001 (full curriculum): ✅ Phases 3-6
- SC-002 (3 exercises/chapter): ✅ All chapter tasks
- SC-003 (valid code): ✅ CodeBlock component, examples/
- SC-004 (alt text): ✅ Image tasks
- SC-005 (3-click nav): ✅ T003, T040
- SC-006 (<3s load): ✅ T044 Lighthouse
- SC-007 (Lighthouse ≥90): ✅ T044
- SC-008 (CI deploys): ✅ T005, T045
````
