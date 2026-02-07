"""FastAPI application entry point."""
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
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://localhost:3001",  # Alternative port
    "http://148.116.94.66:3000",  # Production frontend (OKE LoadBalancer)
    "http://151.145.37.198:8000",  # Backend external IP (for testing)
    "*",  # Allow all origins (for development - restrict in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

