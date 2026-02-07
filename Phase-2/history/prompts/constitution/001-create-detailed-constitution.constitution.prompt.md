---
id: 001
title: Create Detailed Constitution File
stage: constitution
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-todo-cli
user: Maheen-Arif
command: /sp.constitution
labels: ["constitution", "initialization", "spec-driven-development", "monorepo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation artifact)
---

## Prompt

create a deatiled constitution file for my project Hackathon II: Spec-Driven Development
Monorepo Organization For Full-Stack Projects With GitHub
Spec-Kit + Claude Code
This guide explains how to organize your Full-Stack Projects in a monorepo to integrate
GitHub Spec-Kit for spec-driven development with Claude Code. This guide explains how
to organize your repository so that Claude Code and Spec-Kit Plus can effectively edit both
frontend (Next.js) and backend (FastAPI) code in a single context.
Spec-Kit Monorepo Folder Structure
hackathon-todo/
├── .spec-kit/ # Spec-Kit configuration
│ └── config.yaml
├── specs/ # Spec-Kit managed specifications
│ ├── overview.md # Project overview
│ ├── architecture.md # System architecture
│ ├── features/ # Feature specifications
│ │ ├── task-crud.md
│ │ ├── authentication.md
│ │ └── chatbot.md
├── api/ # API specifications
│ │ ├── rest-endpoints.md
│ │ └── mcp-tools.md
│ ├── database/ # Database specifications
│ │ └── schema.md
│ └── ui/ # UI specifications
│ ├── components.md
│ └── pages.md
├── CLAUDE.md # Root Claude Code instructions
├── frontend/
│ ├── CLAUDE.md
│ └── ... (Next.js app)
├── backend/
│ ├── CLAUDE.md
│ └── ... (FastAPI app)
├── docker-compose.yml
└── README.md

[Full user input included monorepo structure, CLAUDE.md patterns, technology stack details (Next.js 14, FastAPI, SQLModel, Neon PostgreSQL, Better Auth), spec organization, and workflow examples]

## Response snapshot

Created comprehensive constitution v1.0.0 for Hackathon II: Spec-Driven Development project with:

**7 Core Principles**:
1. Spec-Driven Development (Non-Negotiable) - All features begin with specifications
2. Monorepo Organization - Clean frontend/backend separation with Spec-Kit integration
3. API-First Design - Contracts defined before implementation
4. Database Schema Management - SQLModel ORM with strict governance
5. Authentication & Authorization - Better Auth with JWT enforcement
6. Frontend Component Standards - Next.js 14 Server Components first, TypeScript strict
7. Testing & Quality (Conditional) - TDD when requested, manual validation otherwise

**Technology Standards**: Documented full stack (Next.js 14, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)

**Development Workflow**: 5-phase lifecycle (Specify → Plan → Tasks → Implement → Review) with PHR and ADR policies

**Governance**: Constitution authority, amendment process, compliance review, complexity justification

All placeholders filled, no unresolved tokens, version 1.0.0 ratified 2026-01-01.

## Outcome

- ✅ Impact: Initial constitution created establishing governance and development standards for full-stack monorepo
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: .specify/memory/constitution.md (created)
- 🔁 Next prompts: Begin feature specification with /sp.specify, or initialize project structure
- 🧠 Reflection: Constitution successfully captures monorepo-specific requirements and integrates Spec-Kit conventions with full-stack best practices

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation - PASS (all placeholders filled, semantic versioning correct, template alignment verified)
- Prompt variant (if applicable): N/A (initial constitution)
- Next experiment (smallest change to try): Monitor constitution usage during first feature implementation to identify missing principles or unclear guidance
