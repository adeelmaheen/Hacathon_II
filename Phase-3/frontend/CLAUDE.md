# Frontend Guidelines - Phase II

## Tech Stack

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Axios (API calls)

## Project Structure

```
app/
├── page.tsx              # Login/Signup page
├── layout.tsx            # Root layout
└── dashboard/
    └── page.tsx          # Todo dashboard

components/ui/
├── task-card.tsx         # Display single task
└── task-form.tsx         # Add/edit task form

lib/
├── api.ts                # Backend API client
└── auth.ts               # JWT token management

types/
└── index.ts              # TypeScript types
```

## TypeScript Types

```typescript
// types/index.ts

export interface User {
  id: number;
  email: string;
  name: string;
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
```

## API Client Pattern

```typescript
// lib/api.ts

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  signup: (data: SignupRequest) => api.post('/api/auth/signup', data),
  login: (data: LoginRequest) => api.post('/api/auth/login', data),
};

export const taskAPI = {
  list: (userId: number) => api.get(`/api/${userId}/tasks`),
  create: (userId: number, data: Partial<Task>) => 
    api.post(`/api/${userId}/tasks`, data),
  update: (userId: number, taskId: number, data: Partial<Task>) => 
    api.put(`/api/${userId}/tasks/${taskId}`, data),
  delete: (userId: number, taskId: number) => 
    api.delete(`/api/${userId}/tasks/${taskId}`),
  toggleComplete: (userId: number, taskId: number) => 
    api.patch(`/api/${userId}/tasks/${taskId}/complete`),
};
```

## Authentication Flow

### Login Page (app/page.tsx)

- Show login/signup form
- On success, save token to localStorage
- Redirect to /dashboard

### Dashboard Page (app/dashboard/page.tsx)

- Check if token exists
- If no token, redirect to /
- Fetch tasks from API
- Display tasks
- Allow CRUD operations

### Token Management (lib/auth.ts)

```typescript
export const auth = {
  setToken: (token: string) => localStorage.setItem('token', token),
  getToken: () => localStorage.getItem('token'),
  removeToken: () => localStorage.removeItem('token'),
  isAuthenticated: () => !!localStorage.getItem('token'),
};
```

## Component Patterns

### Server Components (Default)

Use for static content, no interactivity needed

### Client Components ('use client')

Use for:

- Forms with useState
- Event handlers (onClick, onChange)
- useEffect for data fetching
- localStorage access

## Styling with Tailwind

### Common Patterns

```tsx
// Button
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
  Add Task
</button>

// Input
<input 
  className="border border-gray-300 rounded px-3 py-2 w-full"
  type="text"
/>

// Card
<div className="bg-white shadow rounded p-4">
  {/* content */}
</div>
```

## Data Fetching

### Use Client Component

```tsx
'use client';

import { useEffect, useState } from 'react';
import { taskAPI } from '@/lib/api';

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await taskAPI.list(userId);
      setTasks(response.data);
    } catch (error) {
      console.error('Failed to load tasks');
    }
  };

  return <div>{/* render tasks */}</div>;
}
```

## Error Handling

### Show User-Friendly Messages

```tsx
const [error, setError] = useState('');

try {
  await taskAPI.create(userId, data);
} catch (err: any) {
  if (err.response?.status === 401) {
    setError('Please login again');
  } else {
    setError('Failed to create task');
  }
}
```

## Environment Variables

### .env.local

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Usage

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL;
```

## Development Commands

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Testing Checklist

- [ ] Login with valid credentials
- [ ] Login with invalid credentials shows error
- [ ] Signup creates new user
- [ ] After login, redirects to dashboard
- [ ] Dashboard shows user's tasks only
- [ ] Can add new task
- [ ] Can edit task
- [ ] Can delete task
- [ ] Can mark task complete
- [ ] Logout removes token and redirects

## Common Issues

### CORS Error

- Backend must allow frontend origin
- Check FastAPI CORS middleware

### Token Not Sent

- Verify axios interceptor is set up
- Check token is in localStorage

### Redirect Not Working

- Use useRouter from 'next/navigation'
- Call router.push('/dashboard')

### Data Not Updating

- Call loadTasks() after create/update/delete

## Remember

- Use 'use client' for interactive components
- Always handle loading states
- Show error messages to users
- Validate forms before submitting
- Keep API calls in lib/api.ts

