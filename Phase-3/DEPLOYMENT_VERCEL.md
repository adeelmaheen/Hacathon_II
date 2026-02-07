# Vercel Deployment Guide (Frontend & Backend)

Since you want to deploy **everything for free** using Vercel, follow these steps.

## Part 1: Deploy Backend (FastAPI) to Vercel

1.  **Push your code to GitHub.**
2.  Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
3.  Import your `Hackathon-2-phase-3` (or similar) repository.
4.  **Configure Project:**
    *   **Project Name:** `phase3-backend` (or similar)
    *   **Root Directory:** Click "Edit" and select `Phase-3/backend`.
    *   **Framework Preset:** Select **Other**.
    *   **Environment Variables:** Add the contents of your `Phase-3/backend/.env` file here:
        *   `DATABASE_URL`: (Your Neon DB URL)
        *   `SECRET_KEY`: (Your secret key)
        *   `ALGORITHM`: `HS256`
        *   `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
        *   `OPENAI_API_KEY`: (Your OpenAI Key)
5.  Click **Deploy**.
6.  Once deployed, Vercel will give you a domain (e.g., `https://phase3-backend.vercel.app`).
    *   **Copy this URL.** You will need it for the frontend.

## Part 2: Deploy Frontend (Next.js) to Vercel

1.  Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
2.  Import the **same** repository again.
3.  **Configure Project:**
    *   **Project Name:** `phase3-frontend` (or similar)
    *   **Root Directory:** Click "Edit" and select `Phase-3/frontend`.
    *   **Framework Preset:** Next.js (should be auto-detected).
    *   **Environment Variables:**
        *   **Key:** `NEXT_PUBLIC_API_URL`
        *   **Value:** `https://phase3-backend.vercel.app` (The URL you copied in Part 1).
            *   *Important:* Do not add a trailing slash `/` at the end.
4.  Click **Deploy**.

## Troubleshooting

-   **Backend:** If you see "404 Not Found" on the backend root URL, try `https://phase3-backend.vercel.app/docs` or `https://phase3-backend.vercel.app/health` (if those endpoints exist).
-   **Frontend:** If the frontend can't fetch data, open the browser console (F12) and check if the API requests are going to the correct URL.
