# Deployment Guide

This guide will help you deploy the backend to Render and the frontend to Vercel.

## Prerequisites

- GitHub account (for connecting repositories)
- Render account (https://render.com)
- Vercel account (https://vercel.com)
- Neon PostgreSQL database (https://neon.tech) or any PostgreSQL database

## Backend Deployment (Render)

### Step 1: Prepare Your Repository

1. Make sure all your backend code is committed and pushed to GitHub
2. Ensure `requirements.txt` and `render.yaml` are in the `backend/` directory

### Step 2: Create a Render Web Service

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `todo-api` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables

In Render dashboard, go to your service → Environment → Add the following:

```
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-super-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key-if-needed
FRONTEND_URL=https://your-app.vercel.app
ENVIRONMENT=production
```

**Important Notes:**
- `DATABASE_URL`: Get this from your Neon database or PostgreSQL provider
- `SECRET_KEY`: Generate a secure random string (min 32 chars)
  ```python
  import secrets
  print(secrets.token_urlsafe(32))
  ```
- `FRONTEND_URL`: Will be your Vercel deployment URL (update after frontend deployment)

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your backend
3. Wait for deployment to complete
4. Copy your backend URL (e.g., `https://todo-api.onrender.com`)

### Step 5: Test Your Backend

Visit your backend URL:
- API: `https://your-backend.onrender.com`
- Health Check: `https://your-backend.onrender.com/health`
- API Docs: `https://your-backend.onrender.com/docs`

## Frontend Deployment (Vercel)

### Step 1: Prepare Your Repository

1. Make sure all your frontend code is committed and pushed to GitHub
2. Ensure `vercel.json` is in the `frontend/` directory

### Step 2: Import Project to Vercel

1. Go to https://vercel.com and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `.next` (or leave default)
   - **Install Command**: `npm install` (or leave default)

### Step 3: Configure Environment Variables

In Vercel project settings → Environment Variables → Add:

```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

**Important:**
- Replace `https://your-backend.onrender.com` with your actual Render backend URL
- The `NEXT_PUBLIC_` prefix makes this variable available in the browser

### Step 4: Deploy

1. Click "Deploy"
2. Vercel will automatically build and deploy your frontend
3. Wait for deployment to complete
4. Copy your frontend URL (e.g., `https://your-app.vercel.app`)

### Step 5: Update Backend CORS

1. Go back to Render dashboard
2. Update the `FRONTEND_URL` environment variable with your Vercel URL
3. Redeploy the backend service (or it will auto-redeploy)

## Post-Deployment Checklist

- [ ] Backend is accessible at Render URL
- [ ] Frontend is accessible at Vercel URL
- [ ] Frontend can communicate with backend (check browser console)
- [ ] Database connection is working
- [ ] Authentication is working
- [ ] CORS is properly configured

## Troubleshooting

### Backend Issues

**Database Connection Failed:**
- Verify `DATABASE_URL` is correct in Render environment variables
- Check if your database allows connections from Render's IPs
- For Neon, ensure connection pooling is configured correctly

**CORS Errors:**
- Verify `FRONTEND_URL` in Render matches your Vercel URL exactly
- Check that the URL includes `https://` protocol
- Restart the backend service after updating environment variables

**Module Not Found:**
- Ensure `requirements.txt` includes all dependencies
- Check build logs in Render dashboard

### Frontend Issues

**API Connection Failed:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check that the backend URL is accessible (try in browser)
- Ensure CORS is configured on backend

**Build Errors:**
- Check build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`
- Verify Node.js version compatibility

**Environment Variables Not Working:**
- Remember: Only variables prefixed with `NEXT_PUBLIC_` are available in browser
- Redeploy after adding new environment variables
- Check variable names match exactly (case-sensitive)

## Environment Variables Summary

### Backend (Render)
```
DATABASE_URL=postgresql://...
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=... (optional)
FRONTEND_URL=https://your-app.vercel.app
ENVIRONMENT=production
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## Monitoring

### Render
- View logs: Render dashboard → Your service → Logs
- Monitor uptime: Render dashboard → Your service → Metrics

### Vercel
- View logs: Vercel dashboard → Your project → Deployments → Click deployment → Logs
- Monitor analytics: Vercel dashboard → Your project → Analytics

## Updating Deployments

### Backend Updates
1. Push changes to GitHub
2. Render will automatically detect and redeploy
3. Or manually trigger redeploy from Render dashboard

### Frontend Updates
1. Push changes to GitHub
2. Vercel will automatically detect and redeploy
3. Or manually trigger redeploy from Vercel dashboard

## Cost Considerations

### Render
- Free tier: 750 hours/month (enough for one service)
- Paid plans start at $7/month per service

### Vercel
- Free tier: Unlimited deployments, 100GB bandwidth
- Hobby plan: $0/month (free forever)
- Pro plan: $20/month per user

## Security Best Practices

1. **Never commit secrets**: Use environment variables only
2. **Use strong SECRET_KEY**: Minimum 32 characters, random
3. **Enable HTTPS**: Both Render and Vercel provide SSL by default
4. **Database security**: Use connection pooling, restrict IP access if possible
5. **API rate limiting**: Consider adding rate limiting in production
6. **CORS**: Only allow your frontend domain, not `*` in production

## Support

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Next.js Docs: https://nextjs.org/docs

