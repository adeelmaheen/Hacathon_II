# Todo Full-Stack Application - Phase IV

A modern full-stack Todo application with AI-powered conversational interface built with Next.js, FastAPI, and OpenAI. Now deployed on Kubernetes!

## 🚀 Tech Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13, SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: JWT tokens
- **AI**: OpenAI GPT-4o-mini with function calling

## 📁 Project Structure

```
todo-fullstack/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── specs/             # Specifications
└── README.md          # This file
```

## 🛠️ Quick Start

### Prerequisites

- Node.js 22+ installed ✅ (You have v24.11.1)
- Python 3.13+ installed ✅ (You have v3.13.9)
- UV package manager installed ✅
- Neon PostgreSQL database account (Sign up at https://neon.tech)

### Step 1: Backend Setup

1. **Create Neon Database:**
   - Go to https://neon.tech and sign up
   - Create a new project
   - Copy the connection string

2. **Configure Backend:**
   ```bash
   cd backend
   ```
   
   Create `.env` file (see `backend/SETUP.md` for details):
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/neondb
   SECRET_KEY=your-super-secret-key-min-32-chars
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx  # Get from https://platform.openai.com
   ```

3. **Run Backend:**
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```
   
   Backend will be available at http://localhost:8000

### Step 2: Frontend Setup

1. **Configure Frontend:**
   ```bash
   cd frontend
   ```
   
   Create `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. **Run Frontend:**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at http://localhost:3000

### Step 3: Test the Application

1. Open http://localhost:3000 in your browser
2. Sign up with a new account
3. Create your first task!
4. Test all CRUD operations

## 📚 API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Authentication

All task endpoints require JWT authentication. Include token in header:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## 🎯 Features

### Phase II Features
- User signup and login
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- User-specific task isolation
- Modern, responsive UI

### Phase III Features (NEW! 🤖)
- **AI Chatbot Interface** - Natural language task management
- **Conversational AI** - Chat with your todo assistant
- **Smart Task Management** - Add, view, update, delete tasks via chat
- **Conversation History** - Persistent chat sessions
- **OpenAI Integration** - Powered by GPT-4o-mini

## 💬 AI Chatbot Examples

```
You: "Add a task to buy groceries"
Bot: "✓ I've added 'Buy groceries' to your tasks!"

You: "Show me all my tasks"
Bot: "You have 3 tasks:
     1. Buy groceries (pending)
     2. Call mom (pending)
     3. Finish report (pending)"

You: "Mark task 1 as complete"
Bot: "✓ 'Buy groceries' marked as complete!"
```

## 🚀 Phase IV: Kubernetes Deployment

The application is now containerized and ready for Kubernetes deployment using Minikube!

### Quick Start (Kubernetes)

1. **Prerequisites**: Install Docker Desktop, Minikube, kubectl, and Helm
2. **Build Images**: See [PHASE4_DEPLOYMENT.md](./PHASE4_DEPLOYMENT.md)
3. **Deploy**: Use the Helm chart in `helm/todo-chatbot/`

**📖 Complete Step-by-Step Guide**: See [PHASE4_COMPLETE_GUIDE.md](./PHASE4_COMPLETE_GUIDE.md) for A-Z commands with explanations

**Detailed instructions**: See [PHASE4_DEPLOYMENT.md](./PHASE4_DEPLOYMENT.md)

### Features
- ✅ Docker containerization (Backend + Frontend)
- ✅ Helm charts for Kubernetes deployment
- ✅ Minikube local cluster support
- ✅ AI-assisted operations (kubectl-ai, kagent, Gordon)
- ✅ Production-ready configuration

## 📝 License

MIT

