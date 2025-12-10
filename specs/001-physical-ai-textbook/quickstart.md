# Quickstart Guide

> Physical AI & Humanoid Robotics Textbook - Development Setup

## Prerequisites

| Tool | Version | Installation |
|------|---------|--------------|
| Node.js | ≥18.x | [nodejs.org](https://nodejs.org/) |
| Python | ≥3.11 | [python.org](https://python.org/) |
| pnpm | ≥8.x | `npm install -g pnpm` |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

## Environment Variables

Create `.env` in the project root:

```bash
# Required
OPENAI_API_KEY=sk-...           # OpenAI API key
QDRANT_URL=https://...          # Qdrant Cloud endpoint
QDRANT_API_KEY=...              # Qdrant Cloud API key

# Optional
OPENAI_MODEL=gpt-4o-mini        # Default: gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small  # Default: text-embedding-3-small
```

## Quick Setup

```bash
# Clone and enter project
git clone <repo-url>
cd my-ai-book

# Install all dependencies
pnpm install           # Frontend (Docusaurus)
cd api && uv sync      # Backend (FastAPI)
cd ..

# Start development servers
pnpm dev               # Docusaurus on localhost:3000
pnpm dev:api           # FastAPI on localhost:8000
```

## Project Structure

```
my-ai-book/
├── docusaurus.config.ts    # Site configuration
├── docs/                   # MDX content (chapters)
│   ├── intro.md
│   └── module-*/           # Module folders
├── src/
│   ├── components/         # React components
│   │   ├── ChatWidget/     # RAG chatbot widget
│   │   └── GlossaryTooltip/
│   └── pages/              # Custom pages
├── api/                    # FastAPI backend
│   ├── main.py             # Entry point
│   ├── routes/
│   │   └── chat.py         # /api/chat endpoint
│   ├── services/
│   │   ├── rag.py          # RAG pipeline
│   │   ├── embeddings.py   # Vector operations
│   │   └── llm.py          # OpenAI client
│   └── scripts/
│       └── ingest.py       # Content indexer
├── specs/                  # Feature specifications
└── .env                    # Environment variables (git-ignored)
```

## Common Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start Docusaurus dev server |
| `pnpm build` | Build static site |
| `pnpm dev:api` | Start FastAPI dev server |
| `pnpm ingest` | Index content into Qdrant |
| `pnpm test` | Run Jest tests |
| `pnpm test:api` | Run pytest |
| `pnpm test:e2e` | Run Playwright tests |

## Development Workflow

1. **Content Authoring**: Add/edit MDX files in `docs/`
2. **Re-index**: Run `pnpm ingest` after content changes
3. **Test Chat**: Open site, use chatbot widget to verify RAG
4. **Deploy**: Push to main → Vercel auto-deploys

## Deployment

Vercel handles both static site and serverless functions:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy (first time - links to project)
vercel

# Production deploy
vercel --prod
```

### Vercel Configuration

The `vercel.json` routes `/api/*` to Python serverless functions:

```json
{
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.11"
    }
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "OPENAI_API_KEY not set" | Check `.env` file exists and is loaded |
| Qdrant connection failed | Verify `QDRANT_URL` and `QDRANT_API_KEY` |
| Chatbot returns empty | Run `pnpm ingest` to index content |
| Build fails on Vercel | Check Node.js version matches (≥18) |

## Next Steps

1. Review `specs/001-physical-ai-textbook/spec.md` for requirements
2. Check `plan.md` for architecture decisions
3. See `data-model.md` for entity definitions
4. Read `contracts/openapi.yaml` for API specification
