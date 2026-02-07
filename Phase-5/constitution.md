# Project Constitution

## Project Overview
This is a full-stack Todo application built as part of a hackathon project.

## Tech Stack
- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13, SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: JWT tokens

## Development Principles
1. **Spec-Driven Development**: Specifications first, then code
2. **Type Safety**: Use TypeScript (frontend) and type hints (backend)
3. **Security**: Never store plain passwords, always verify JWT tokens
4. **User Isolation**: Each user can only access their own tasks
5. **Error Handling**: Always handle errors gracefully with user-friendly messages

## Project Structure
```
todo-fullstack/
├── constitution.md
├── CLAUDE.md
├── README.md
├── docker-compose.yml
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── features/
│   ├── api/
│   ├── database/
│   └── ui/
├── frontend/
│   └── (Next.js app)
└── backend/
    └── (FastAPI app)
```

## Code Standards
- Follow language-specific style guides
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Use meaningful variable names

## Git Workflow
- Commit frequently with clear messages
- Push to main branch
- Keep commits atomic (one feature per commit)

