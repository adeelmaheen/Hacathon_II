# Backend Guidelines - Phase II

## Tech Stack

- FastAPI (Python web framework)
- SQLModel (ORM for PostgreSQL)
- Neon PostgreSQL (cloud database)
- JWT authentication

## Project Structure

```
app/
├── main.py          # FastAPI app, CORS setup
├── models.py        # User, Task models
├── database.py      # Database connection
├── auth.py          # JWT token handling
├── config.py        # Environment variables
└── routes/
    ├── tasks.py     # CRUD endpoints
    └── auth.py      # Login/signup
```

## Database Models

### User Model

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Endpoints Required

### Authentication

- POST /api/auth/signup - Register new user
- POST /api/auth/login - Login and get JWT token

### Tasks (All require JWT token)

- GET /api/{user_id}/tasks - List all user's tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{id} - Get specific task
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle complete status

## Security Rules

### JWT Authentication

- Every task endpoint must verify JWT token
- Extract user_id from token
- Match token user_id with URL user_id
- Return 401 if unauthorized

### Password Handling

- Use bcrypt for hashing
- Never store plain passwords
- Hash before saving to database

## CORS Configuration

Allow frontend origin:

```python
origins = [
    "http://localhost:3000",  # Next.js dev
    "https://your-app.vercel.app"  # Production
]
```

## Environment Variables (.env file)

```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Error Handling

- 400 Bad Request - Invalid input
- 401 Unauthorized - No/invalid token
- 403 Forbidden - Token user_id doesn't match URL
- 404 Not Found - Task/user not found
- 500 Internal Server Error - Database errors

## Code Standards

- Type hints on all functions
- Pydantic models for request/response
- Async/await for database operations
- Try-except for error handling
- Clear error messages

## Development Commands

```bash
# Run server
uvicorn app.main:app --reload --port 8000

# Create database tables
# (Auto-creates on first run)
```

## Testing Endpoints

Use curl or Postman:

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123","name":"Test"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}'

# Get tasks (with token)
curl http://localhost:8000/api/1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Common Issues

### Database Connection Failed

- Check DATABASE_URL in .env
- Verify Neon database is active
- Check internet connection

### CORS Error

- Add frontend URL to origins list
- Restart FastAPI server

### 401 Unauthorized

- Check token is being sent in header
- Verify token hasn't expired
- Check SECRET_KEY matches

## Remember

- Always validate user_id from token matches URL
- Use async functions for database
- Handle all exceptions
- Return proper HTTP status codes

