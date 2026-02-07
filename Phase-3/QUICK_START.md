# Quick Start Guide - Phase II

## ✅ What's Already Done

All code has been generated! You just need to:

1. Set up your Neon database
2. Configure environment variables
3. Run both servers

## 🚀 Step-by-Step Setup

### 1. Get Neon Database URL

1. Visit https://neon.tech
2. Sign up (free tier is fine)
3. Click "Create Project"
4. Name it: `todo-app`
5. Select region closest to you
6. Click "Create Project"
7. Copy the connection string (looks like: `postgresql://user:pass@ep-xxx.neon.tech/neondb`)

### 2. Configure Backend

```bash
cd backend
```

Create a file named `.env` (no extension) with:

```env
DATABASE_URL=postgresql://your-actual-neon-url-here
SECRET_KEY=change-this-to-a-random-32-character-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**To generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Start Backend

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test it: Open http://localhost:8000/docs in your browser

### 4. Configure Frontend

Open a **new terminal** (keep backend running):

```bash
cd frontend
```

Create a file named `.env.local` with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Start Frontend

```bash
npm run dev
```

You should see:
```
✓ Ready in Xms
○ Local: http://localhost:3000
```

### 6. Test the App!

1. Open http://localhost:3000
2. Click "Sign up"
3. Enter:
   - Name: Your Name
   - Email: test@example.com
   - Password: password123
4. Click "Sign Up"
5. You'll be redirected to dashboard
6. Click "+ Add New Task"
7. Create a task and test all features!

## 🐛 Troubleshooting

### Backend won't start

**Error: "DATABASE_URL not found"**
- Make sure `.env` file exists in `backend/` folder
- Check file name is exactly `.env` (not `.env.txt`)

**Error: "Connection refused"**
- Check your Neon database is active
- Verify DATABASE_URL is correct
- Make sure you copied the full connection string

### Frontend won't connect to backend

**Error: "Network Error" or CORS error**
- Make sure backend is running on port 8000
- Check `.env.local` has correct URL
- Restart frontend after changing `.env.local`

### Can't login/signup

**Error: "Authentication failed"**
- Check backend is running
- Check browser console for errors
- Verify DATABASE_URL is correct in backend `.env`

## 📝 Next Steps

Once everything is working:

1. ✅ Test all features (create, edit, delete, complete tasks)
2. ✅ Check Swagger UI at http://localhost:8000/docs
3. ✅ Try logging out and logging back in
4. ✅ Create multiple users and verify isolation

## 🎉 You're Done!

Your full-stack Todo app is ready! All Phase II requirements are complete.

