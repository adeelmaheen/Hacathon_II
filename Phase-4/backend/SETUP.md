# Backend Setup Instructions

## 🛠️ Local Development Setup

Follow these steps to run the backend locally.

### 1. Prerequisites
- Python 3.11+
- pip (Python package manager)

### 2. Set up Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages using pip:

```bash
pip install -e .
```

### 4. Configure Environment Variables
Create a `.env` file in the `backend` directory (or copy from a template if available).

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=sk-proj-your-openai-key
```

### 5. Setup Neon Database (PostgreSQL)
1. Go to [Neon console](https://console.neon.tech/).
2. Sign up or Log in.
3. Click **"New Project"**.
4. Give it a name (e.g., `hackathon-phase4`) and select a region.
5. Click **"Create Project"**.
6. On the **Dashboard**, look for the **Connection Details** section.
7. Switch the view to **"Parameters"** or copy the **"Connection String"** directly.
   - It should look like: `postgresql://neondb_owner:xxxxx@ep-xyz.aws.neon.tech/neondb?sslmode=require`
8. Paste this string into your `.env` file as `DATABASE_URL`.

### 6. Run the Backend Server
Start the FastAPI server using uvicorn:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API Root:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

