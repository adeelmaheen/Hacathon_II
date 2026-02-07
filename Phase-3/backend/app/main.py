"""FastAPI application entry point."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth, tasks, chat

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Full-stack Todo application API",
    version="1.0.0"
)

# CORS configuration
# Allow localhost for development and Vercel domains for production
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://localhost:3001",  # Alternative port
]

# Add production frontend URL from environment variable
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    origins.append(frontend_url)

# Allow Vercel preview deployments if enabled (for PR previews)
allow_vercel_previews = os.getenv("ALLOW_VERCEL_PREVIEWS", "false").lower() == "true"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app" if allow_vercel_previews else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    init_db()

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo API is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

