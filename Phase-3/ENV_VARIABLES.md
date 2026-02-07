# Environment Variables Reference

## Backend (Render)

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | Secret key for JWT tokens (min 32 chars) | `your-secret-key-here` |
| `FRONTEND_URL` | Your Vercel frontend URL | `https://your-app.vercel.app` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ALGORITHM` | JWT algorithm | `HS256` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` | `60` |
| `OPENAI_API_KEY` | OpenAI API key (if using chat features) | - | `sk-...` |
| `ENVIRONMENT` | Environment name | `development` | `production` |
| `ALLOW_VERCEL_PREVIEWS` | Allow Vercel preview deployments | `false` | `true` |

## Frontend (Vercel)

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Your Render backend URL | `https://todo-api.onrender.com` |

**Note:** Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## Generating a Secret Key

### Python
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Node.js
```javascript
require('crypto').randomBytes(32).toString('base64')
```

### Online
Use a secure random string generator (minimum 32 characters)

## Setting Up Environment Variables

### Render
1. Go to your service dashboard
2. Navigate to "Environment"
3. Add each variable with its value
4. Click "Save Changes"
5. Service will automatically redeploy

### Vercel
1. Go to your project dashboard
2. Navigate to "Settings" → "Environment Variables"
3. Add each variable with its value
4. Select environment (Production, Preview, Development)
5. Click "Save"
6. Redeploy your application

## Security Best Practices

1. **Never commit** `.env` files to git
2. **Use strong secrets**: Minimum 32 characters for SECRET_KEY
3. **Rotate secrets** periodically in production
4. **Restrict access**: Only give team members who need it access to env vars
5. **Use different values** for development and production
6. **Validate URLs**: Ensure FRONTEND_URL and NEXT_PUBLIC_API_URL use HTTPS in production

