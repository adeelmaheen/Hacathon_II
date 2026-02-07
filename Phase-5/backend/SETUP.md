# Backend Setup Instructions

## Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Getting Your Database URL

1. Go to https://neon.tech
2. Sign up or log in
3. Create a new project
4. Copy the connection string from the dashboard
5. Replace `postgresql://` with `postgresql://` (should already be correct)

### Generating a Secret Key

You can generate a secure secret key using Python:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use any random string generator (minimum 32 characters recommended).

## Running the Backend

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

