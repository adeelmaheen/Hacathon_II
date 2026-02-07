"""
FastAPI main application entry point.
Configures CORS, includes routers, and defines app metadata.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import auth, tasks

app = FastAPI(
    title="Todo Application API",
    description="REST API for full-stack todo web application with authentication",
    version="1.0.0",
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Todo API is running"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {"status": "healthy", "service": "todo-api"}
