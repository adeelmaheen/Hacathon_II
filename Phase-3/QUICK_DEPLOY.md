# Quick Deployment Guide

## 🚀 Quick Start

### Backend (Render) - 5 Minutes

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push
   ```

2. **Create Render Service**
   - Go to https://render.com → New Web Service
   - Connect GitHub repo
   - Settings:
     - Root Directory: `backend`
     - Build: `pip install -r requirements.txt`
     - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables (see ENV_VARIABLES.md)
   - Deploy!

3. **Get Backend URL**
   - Copy URL from Render dashboard (e.g., `https://todo-api.onrender.com`)

### Frontend (Vercel) - 3 Minutes

1. **Deploy to Vercel**
   - Go to https://vercel.com → Add Project
   - Import GitHub repo
   - Settings:
     - Root Directory: `frontend`
     - Framework: Next.js (auto-detected)
   - Add Environment Variable:
     - `NEXT_PUBLIC_API_URL` = Your Render backend URL
   - Deploy!

2. **Get Frontend URL**
   - Copy URL from Vercel dashboard (e.g., `https://your-app.vercel.app`)

3. **Update Backend CORS**
   - Go back to Render
   - Update `FRONTEND_URL` = Your Vercel URL
   - Redeploy backend

## ✅ Done!

Your app is now live! 🎉

- Frontend: `https://your-app.vercel.app`
- Backend: `https://todo-api.onrender.com`
- API Docs: `https://todo-api.onrender.com/docs`

## 📝 Required Environment Variables

### Backend (Render)
```
DATABASE_URL=postgresql://...
SECRET_KEY=... (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
FRONTEND_URL=https://your-app.vercel.app
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://todo-api.onrender.com
```

## 🔧 Troubleshooting

**CORS Error?**
- Check `FRONTEND_URL` in Render matches your Vercel URL exactly
- Ensure URL includes `https://`

**Database Error?**
- Verify `DATABASE_URL` is correct
- Check database is accessible from Render

**Build Failed?**
- Check build logs in Render/Vercel dashboard
- Ensure all dependencies are in `requirements.txt` / `package.json`

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

