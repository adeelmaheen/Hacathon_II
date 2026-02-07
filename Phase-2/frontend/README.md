# Todo Web App - Frontend

Modern, responsive task management application built with Next.js 14, TypeScript, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.0+ (strict mode)
- **Styling**: Tailwind CSS 3
- **State Management**: React hooks + SWR for data fetching
- **Forms**: React Hook Form + Zod validation
- **API Client**: Custom fetch-based client with TypeScript

## Features

- ✅ User authentication (register, login, logout)
- ✅ Create, read, update, delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task titles and descriptions
- ✅ Optimistic UI updates for instant feedback
- ✅ Real-time data synchronization with SWR
- ✅ Responsive design (320px to 4K)
- ✅ Accessible UI (WCAG 2.1 AA compliant)
- ✅ Loading and error states

## Prerequisites

- Node.js 18+ or 20+
- npm, yarn, or pnpm
- Backend API running (see backend/README.md)

## Getting Started

### 1. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

### 2. Environment Setup

Create a `.env.local` file in the `frontend/` directory:

```bash
cp .env.local.example .env.local
```

Update the environment variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Environment Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

### 3. Run Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

The application will be available at **http://localhost:3000**

### 4. Build for Production

```bash
npm run build
npm start
# or
yarn build
yarn start
# or
pnpm build
pnpm start
```

## Project Structure

```
frontend/
├── app/                          # Next.js 14 App Router
│   ├── (app)/                   # Authenticated routes
│   │   ├── dashboard/           # Main dashboard page
│   │   └── layout.tsx           # Authenticated layout with header
│   ├── (auth)/                  # Public auth routes
│   │   ├── login/               # Login page
│   │   └── register/            # Registration page
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Landing page (redirects)
│   └── globals.css              # Global styles
├── components/                   # React components
│   ├── auth/                    # Auth components
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── tasks/                   # Task components
│   │   ├── TaskCard.tsx         # Individual task display/edit
│   │   ├── TaskForm.tsx         # Create task form
│   │   ├── TaskList.tsx         # Task list container
│   │   └── EmptyState.tsx       # Empty state message
│   └── ui/                      # Reusable UI components
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Modal.tsx
│       └── Spinner.tsx
├── hooks/                        # Custom React hooks
│   ├── useAuth.tsx              # Authentication state
│   └── useTasks.tsx             # Task management with SWR
├── lib/                          # Utility libraries
│   ├── api.ts                   # API client
│   └── validators.ts            # Zod schemas
├── types/                        # TypeScript definitions
│   ├── user.ts
│   └── task.ts
├── public/                       # Static assets
├── .env.local.example           # Environment template
├── next.config.js               # Next.js config
├── tailwind.config.ts           # Tailwind config
├── tsconfig.json                # TypeScript config
└── package.json
```

## Key Concepts

### App Router (Next.js 14)

This project uses the **App Router** (not Pages Router):

- **Server Components** by default (better performance)
- **Client Components** marked with `"use client"` (for interactivity)
- File-based routing in `app/` directory
- Layouts with nested routing

### Authentication Flow

1. User visits landing page (`/`)
2. Redirected to `/login` if not authenticated
3. After login, redirected to `/dashboard`
4. JWT token stored in HTTPOnly cookie
5. Token included in all API requests via `credentials: 'include'`

### Data Fetching with SWR

Tasks are managed using SWR for:

- **Automatic caching**: No duplicate requests
- **Revalidation**: Data stays fresh
- **Optimistic updates**: Instant UI feedback
- **Error recovery**: Automatic retries

Example:

```typescript
const { tasks, loading, error, createTask, updateTask, deleteTask } = useTasks()
```

### Form Validation

Forms use Zod schemas for client-side validation:

```typescript
const schema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(1000).optional(),
})
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Check TypeScript types |
| `npm run format` | Format code with Prettier |

## API Client Usage

All API calls go through the centralized client in `lib/api.ts`:

```typescript
import * as api from '@/lib/api'

// Authentication
await api.register({ email, name, password })
await api.login({ email, password })
await api.logout()

// Tasks
const tasks = await api.getTasks()
const task = await api.createTask({ title, description })
await api.updateTask(taskId, { title, description })
await api.toggleTask(taskId)
await api.deleteTask(taskId)
```

## Component Patterns

### Server Component (default)

```tsx
// app/dashboard/page.tsx
export default function DashboardPage() {
  return <div>Server Component</div>
}
```

### Client Component (interactive)

```tsx
"use client"

import { useState } from 'react'

export function TaskForm() {
  const [title, setTitle] = useState('')
  // ... interactive logic
}
```

### Optimistic UI Updates

```tsx
const updateTask = async (taskId: number, data: TaskUpdate) => {
  // 1. Optimistically update UI
  mutate(
    (tasks) => tasks.map(t => t.id === taskId ? { ...t, ...data } : t),
    { revalidate: false }
  )

  // 2. Make API request
  await api.updateTask(taskId, data)

  // 3. Revalidate from server
  mutate()
}
```

## Styling with Tailwind CSS

### Utility-First Classes

```tsx
<div className="max-w-4xl mx-auto p-6">
  <h1 className="text-3xl font-bold text-gray-900 mb-4">
    Dashboard
  </h1>
</div>
```

### Responsive Design

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 1 column on mobile, 2 on tablet, 3 on desktop */}
</div>
```

### Custom Components

Reusable components in `components/ui/`:

```tsx
<Button variant="primary" onClick={handleSave}>
  Save Task
</Button>

<Input
  value={title}
  onChange={(e) => setTitle(e.target.value)}
  error={errors.title}
/>
```

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` → Your backend URL
4. Deploy

```bash
vercel --prod
```

### Docker

Build and run with Docker:

```bash
# Build image
docker build -t todo-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://your-backend-url \
  todo-frontend
```

### Other Platforms

The frontend can be deployed to:

- **Netlify**: Static export or Next.js runtime
- **AWS Amplify**: Full Next.js support
- **Cloudflare Pages**: Edge runtime
- **Self-hosted**: Node.js server with PM2

**Build command**: `npm run build`
**Output directory**: `.next/`
**Install command**: `npm install`
**Start command**: `npm start`

## Environment-Specific Configs

### Development

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Troubleshooting

### API Connection Issues

**Problem**: Cannot connect to backend

**Solution**:
1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Ensure CORS is configured in backend

### TypeScript Errors

**Problem**: Type errors in IDE

**Solution**:
```bash
# Restart TypeScript server
npx tsc --noEmit

# Check for errors
npm run type-check
```

### Hydration Errors

**Problem**: "Text content does not match" error

**Solution**:
- Don't use `localStorage` in Server Components
- Wrap client-only code with `typeof window !== 'undefined'`
- Use `"use client"` directive for interactive components

### SWR Cache Issues

**Problem**: Stale data showing

**Solution**:
```typescript
// Force revalidation
const { refresh } = useTasks()
await refresh()
```

## Browser Support

- Chrome/Edge (last 2 years)
- Firefox (last 2 years)
- Safari 15+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

- Keyboard navigation support
- ARIA labels on interactive elements
- Focus management in modals
- Screen reader friendly
- Semantic HTML

## Performance

- Lighthouse scores: 90+ (performance, accessibility, best practices)
- Bundle size target: <500KB (gzipped)
- First Contentful Paint: <1.5s
- Time to Interactive: <3s

## Contributing

1. Follow TypeScript strict mode (no `any` types)
2. Use Prettier for formatting
3. Write accessible components (ARIA labels)
4. Test responsive design (320px - 4K)
5. Use optimistic UI updates for better UX

## License

MIT

## Support

For issues or questions:
- Check the [specification](../specs/001-todo-web-app/spec.md)
- Review the [implementation plan](../specs/001-todo-web-app/plan.md)
- See [backend README](../backend/README.md) for API documentation
