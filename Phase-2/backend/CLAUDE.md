# Backend Guidelines - FastAPI

This file provides backend-specific context for Claude Code when working in the `/backend` directory.

## Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth with JWT
- **Validation**: Pydantic models
- **Python Version**: 3.11+

## Project Structure

```
backend/
├── src/
│   ├── main.py           # FastAPI app entry point
│   ├── db.py             # Database connection and session
│   ├── models/           # SQLModel database models
│   │   ├── user.py
│   │   └── task.py
│   ├── services/         # Business logic layer
│   │   └── task_service.py
│   ├── api/              # API route handlers
│   │   ├── auth.py
│   │   └── tasks.py
│   └── routes/           # Route registration (if separated)
├── tests/
│   ├── contract/         # API contract tests
│   ├── integration/      # Integration tests
│   └── unit/             # Unit tests
├── requirements.txt
└── .env.example
```

## Architecture Patterns

### Layered Architecture

Follow a clean separation of concerns:

1. **Models** (`models/`) - Database schema and ORM
2. **Services** (`services/`) - Business logic
3. **API** (`api/`) - HTTP handlers and routing
4. **Database** (`db.py`) - Connection management

**Example Flow**:
```
HTTP Request → API Handler → Service Layer → Database Model → Database
```

### SQLModel Patterns

```python
# models/task.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Key Points**:
- Use `SQLModel` for both ORM and API validation
- Always add `index=True` for foreign keys and frequently filtered fields
- Use `Optional` for nullable fields
- Set `max_length` for string fields

### Database Connection

```python
# db.py
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

**Usage in routes**:
```python
from fastapi import Depends
from sqlmodel import Session
from db import get_session

@app.get("/api/tasks")
def get_tasks(session: Session = Depends(get_session)):
    # Use session here
    pass
```

## API Conventions

### Route Structure

All API routes MUST be under `/api/` prefix:

```python
# main.py
from fastapi import FastAPI
from api import tasks, auth

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
```

### Request/Response Models

Use Pydantic models for validation:

```python
# api/tasks.py
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from ORM models

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task(**task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Error Handling

Use `HTTPException` for all errors:

```python
from fastapi import HTTPException, status

@router.get("/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task
```

**Common Status Codes**:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid auth
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Authentication & Authorization

### JWT Token Validation

```python
# api/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Protected Endpoints

```python
@router.get("/api/tasks")
def get_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Only return tasks for the authenticated user
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

## Database Operations

### Query Patterns

```python
from sqlmodel import select

# Get all
tasks = session.exec(select(Task)).all()

# Filter
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# Filter with multiple conditions
tasks = session.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .where(Task.completed == False)
).all()

# Get one
task = session.exec(
    select(Task).where(Task.id == task_id)
).first()

# Or use get for primary key
task = session.get(Task, task_id)
```

### CRUD Operations

```python
# Create
new_task = Task(title="New Task", user_id=user_id)
session.add(new_task)
session.commit()
session.refresh(new_task)

# Update
task = session.get(Task, task_id)
task.title = "Updated Title"
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()

# Delete
task = session.get(Task, task_id)
session.delete(task)
session.commit()
```

## Environment Configuration

### Required Environment Variables

```bash
# .env
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Loading Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    class Config:
        env_file = ".env"

settings = Settings()
```

## Testing

### Contract Tests

Test API contracts against specifications:

```python
# tests/contract/test_tasks.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_tasks_returns_array():
    response = client.get("/api/tasks", headers={"Authorization": "Bearer token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Integration Tests

Test user journeys end-to-end:

```python
def test_create_and_retrieve_task():
    # Create task
    response = client.post("/api/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Retrieve task
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
```

## Running the Application

### Development

```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

Access at: `http://localhost:8000`
Docs at: `http://localhost:8000/docs` (Swagger UI)

### With Docker

```bash
docker-compose up backend
```

## Key Conventions

1. **Specs First**: Always read `/specs/api/`, `/specs/database/` before implementing
2. **Reference Specs**: Use `@specs/api/rest-endpoints.md` syntax
3. **All routes under `/api/`**: No exceptions
4. **Use SQLModel**: No raw SQL queries
5. **User isolation**: Always filter by `user_id` from JWT
6. **Environment variables**: All secrets in `.env`
7. **HTTPException for errors**: Consistent error handling
8. **Constitution compliance**: Follow `.specify/memory/constitution.md`

## Common Tasks

### Adding a New Endpoint

1. Read API spec: `@specs/api/rest-endpoints.md`
2. Create Pydantic request/response models
3. Add route handler in `api/[resource].py`
4. Add authentication if needed
5. Query database using SQLModel
6. Return appropriate status code

### Adding a New Model

1. Read database spec: `@specs/database/schema.md`
2. Create SQLModel class in `models/[model].py`
3. Add indexes for foreign keys and filters
4. Run migrations (if using Alembic)
5. Update API models to match

### Adding Business Logic

1. Create service in `services/[service].py`
2. Keep database operations in service layer
3. Call from API route handlers
4. Test independently with unit tests

## References

- Root instructions: `@/CLAUDE.md`
- Constitution: `@.specify/memory/constitution.md`
- Frontend API client: `@frontend/lib/api.ts`
- Specs: `@specs/`
