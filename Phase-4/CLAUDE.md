# Claude Assistant Guidelines

## Project Context
This is Phase II of a hackathon project - converting a console Todo app into a full-stack web application.

## Architecture
```
User Browser (Next.js) 
    ↓ HTTP Requests
Backend API (FastAPI)
    ↓ Database Queries
Neon PostgreSQL
```

## Key Requirements

### Backend (FastAPI)
- Use SQLModel for database models
- JWT authentication for all protected endpoints
- User-specific task isolation (users can only access their own tasks)
- CORS enabled for frontend communication
- Environment variables for configuration

### Frontend (Next.js)
- App Router architecture
- TypeScript for type safety
- Client components for interactivity
- Server components for static content
- Tailwind CSS for styling
- Axios for API calls

## Development Approach
1. Read specifications first
2. Create code following specifications
3. Test each component
4. Integrate step by step

## Common Patterns

### Backend
- Use async/await for database operations
- Validate all inputs with Pydantic
- Return proper HTTP status codes
- Handle exceptions gracefully

### Frontend
- Use 'use client' for interactive components
- Store JWT token in localStorage
- Show loading states during API calls
- Display error messages to users

## Security Rules
- Never expose passwords in responses
- Always verify JWT tokens
- Match user_id from token with request
- Use environment variables for secrets

