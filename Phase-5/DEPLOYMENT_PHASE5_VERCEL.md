# Phase 5 Vercel Deployment Guide

This guide will help you deploy both the Phase 5 Backend (FastAPI) and Frontend (Next.js) to Vercel for free.

## Part 1: Deploy Backend (FastAPI) to Vercel

1.  **Push your code to GitHub.**
2.  Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
3.  Import your `Hackathon-2-phase-5` (or similar) repository.
4.  **Configure Project:**
    *   **Project Name:** `phase5-backend`
    *   **Root Directory:** Click "Edit" and select `Phase-5/backend`.
    *   **Framework Preset:** Select **Other**.
    *   **Environment Variables:** Add the contents of your `Phase-5/backend/.env` file:
        *   `DATABASE_URL`: (Your Neon DB URL)
        *   `SECRET_KEY`: (Your secret key)
        *   `ALGORITHM`: `HS256`
        *   `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
        *   `OPENAI_API_KEY`: (Your OpenAI Key)
5.  Click **Deploy**.
6.  Once deployed, copy the domain (e.g., `https://phase5-backend.vercel.app`).

## Part 2: Deploy Frontend (Next.js) to Vercel

1.  Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
2.  Import the **same** repository again.
3.  **Configure Project:**
    *   **Project Name:** `phase5-frontend`
    *   **Root Directory:** Click "Edit" and select `Phase-5/frontend`.
    *   **Framework Preset:** Next.js (auto-detected).
    *   **Environment Variables:**
        *   **Key:** `NEXT_PUBLIC_API_URL`
        *   **Value:** `https://phase5-backend.vercel.app` (The URL from Part 1).
            *   *Important:* Do NOT add a trailing slash `/`.
4.  Click **Deploy**.

## Troubleshooting

-   **Backend 404:** Try accessing `https://phase5-backend.vercel.app/docs` to see if the API is running.
-   **Frontend API Errors:** Check the browser console (F12) to ensure requests are hitting the correct backend URL.
