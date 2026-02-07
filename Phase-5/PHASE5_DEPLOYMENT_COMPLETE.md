# Phase 5: Advanced Cloud Deployment - Complete Guide

## 📋 Overview

Phase 5 mein humne Todo Chatbot application ko **Oracle Cloud Infrastructure (OCI) - Oracle Kubernetes Engine (OKE)** par deploy kiya. Ye complete guide hai ki kaise deployment hua.

---

## 🎯 Phase 5 Objectives

1. ✅ **Oracle Cloud (OKE) Deployment**
2. ✅ **Docker Image Registry (OCI Container Registry)**
3. ✅ **CI/CD Pipeline (GitHub Actions)**
4. ✅ **Kubernetes Deployment**
5. ✅ **LoadBalancer Services**
6. ✅ **Database Migration**
7. ✅ **CORS Configuration**
8. ✅ **Route Ordering Fix**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Oracle Cloud (OKE)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐            │
│  │   Frontend   │         │   Backend    │            │
│  │  (Next.js)   │─────────▶│  (FastAPI)   │            │
│  │              │         │              │            │
│  │ LoadBalancer │         │ LoadBalancer │            │
│  │  :3000       │         │   :8000      │            │
│  └──────────────┘         └──────────────┘            │
│         │                        │                      │
│         └────────────┬───────────┘                      │
│                      │                                   │
│              ┌───────▼───────┐                          │
│              │  PostgreSQL   │                          │
│              │   (Neon DB)   │                          │
│              └───────────────┘                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
         ▲
         │
         │ Docker Images
         │
┌────────▼──────────────────────────────────────────────┐
│         OCI Container Registry                          │
│  ca-montreal-1.ocir.io/axkmnfbutyiu/todo-app/          │
│    - todo-backend:latest                                │
│    - todo-frontend:latest                               │
└─────────────────────────────────────────────────────────┘
         ▲
         │
         │ GitHub Actions CI/CD
         │
┌────────▼──────────────────────────────────────────────┐
│              GitHub Repository                          │
│         (Auto Build & Push)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Deployment Process

### **Step 1: Oracle Cloud Setup**

#### 1.1 OKE Cluster Create

**Oracle Cloud Console se:**
1. OCI Console → Kubernetes (OKE) → Create Cluster
2. Cluster details:
   - Name: `todo-cluster`
   - Kubernetes Version: Latest
   - Node Pool: 3 nodes (free tier compatible)
   - Shape: VM.Standard.E2.1.Micro (free tier)

**Commands (Cloud Shell):**
```bash
# Cluster info check
oci ce cluster list --compartment-id <compartment-id>

# Kubeconfig download
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-id> \
  --file $HOME/.kube/config \
  --region ca-montreal-1 \
  --token-version 2.0.0

# Verify connection
kubectl get nodes
```

**Output:**
```
NAME          STATUS   ROLES   AGE   VERSION
10.0.10.166   Ready    node    7h    v1.34.2
10.0.10.55    Ready    node    7h    v1.34.2
10.0.10.68    Ready    node    7h    v1.34.2
```

---

### **Step 2: OCI Container Registry Setup**

#### 2.1 Registry Create

**Oracle Cloud Console se:**
1. Developer Services → Container Registry → Create Repository
2. Repository Name: `todo-app`
3. Access: Public (or Private with IAM policies)

**Registry Details:**
- **Region:** `ca-montreal-1`
- **Registry URL:** `ca-montreal-1.ocir.io`
- **Tenancy Namespace:** `axkmnfbutyiu` (from `oci os ns get`)
- **Repository:** `todo-app`

#### 2.2 Auth Token Generate

**Oracle Cloud Console se:**
1. User Settings → Auth Tokens → Generate Token
2. Token name: `oci-registry-token`
3. **Token copy karo** (dobaara nahi milega)

**Username Format:**
```
<tenancy-namespace>/<oci-username>
Example: axkmnfbutyiu/ma9400667@gmail.com
```

---

### **Step 3: GitHub Actions CI/CD Setup**

#### 3.1 GitHub Secrets Configure

**GitHub Repository → Settings → Secrets and variables → Actions:**

Add these secrets:
- `OCI_USERNAME`: `axkmnfbutyiu/ma9400667@gmail.com`
- `OCI_AUTH_TOKEN`: `<your-auth-token>`

#### 3.2 GitHub Actions Workflow

**File:** `.github/workflows/build-push-oci.yml`

```yaml
name: Build and Push to OCI Registry

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  REGION: ca-montreal-1
  TENANCY_NAMESPACE: axkmnfbutyiu
  REGISTRY: ca-montreal-1.ocir.io
  REPO_NAME: todo-app

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to OCI Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.OCI_USERNAME }}
          password: ${{ secrets.OCI_AUTH_TOKEN }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          platforms: linux/amd64
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.TENANCY_NAMESPACE }}/${{ env.REPO_NAME }}/todo-backend:latest
            ${{ env.REGISTRY }}/${{ env.TENANCY_NAMESPACE }}/${{ env.REPO_NAME }}/todo-backend:${{ github.sha }}

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          platforms: linux/amd64
          build-args: |
            NEXT_PUBLIC_API_URL=http://151.145.37.198:8000
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.TENANCY_NAMESPACE }}/${{ env.REPO_NAME }}/todo-frontend:latest
            ${{ env.REGISTRY }}/${{ env.TENANCY_NAMESPACE }}/${{ env.REPO_NAME }}/todo-frontend:${{ github.sha }}
```

**Key Points:**
- ✅ `platforms: linux/amd64` - OKE nodes x86_64 architecture ke hain
- ✅ `NEXT_PUBLIC_API_URL` - Frontend ko backend URL pata hona chahiye
- ✅ Auto-trigger on `main` branch push

---

### **Step 4: Cloud Shell Setup**

#### 4.1 Repository Clone

**Cloud Shell mein:**
```bash
# GitHub Personal Access Token use karo
git clone https://ghp_<YOUR_TOKEN>@github.com/muzaffar401/Hackathon-2-phase-4.git

cd Hackathon-2-phase-4
```

**GitHub PAT Setup:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate token with `repo` scope
3. Token use karo clone ke liye

---

### **Step 5: Kubernetes Deployment**

#### 5.1 Namespace Create

```bash
kubectl create namespace todo-app
```

#### 5.2 Secrets Create

```bash
# Database and API keys
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://neondb_owner:KeTzbt4l9aic@ep-raspy-mouse-a4y26s5i-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" \
  --from-literal=SECRET_KEY="$(openssl rand -hex 32)" \
  --from-literal=OPENAI_API_KEY="sk-proj-..." \
  -n todo-app
```

#### 5.3 Backend Deployment

**File:** `k8s/backend-deployment.yaml` (or inline)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
    spec:
      containers:
      - name: backend
        image: ca-montreal-1.ocir.io/axkmnfbutyiu/todo-app/todo-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: DATABASE_URL
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: SECRET_KEY
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: OPENAI_API_KEY
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  type: LoadBalancer
  selector:
    app: todo-backend
  ports:
  - port: 8000
    targetPort: 8000
```

**Apply:**
```bash
kubectl apply -f k8s/backend-deployment.yaml
```

#### 5.4 Frontend Deployment

**File:** `k8s/frontend-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: frontend
        image: ca-montreal-1.ocir.io/axkmnfbutyiu/todo-app/todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://151.145.37.198:8000"  # Backend LoadBalancer IP
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: todo-app
spec:
  type: LoadBalancer
  selector:
    app: todo-frontend
  ports:
  - port: 3000
    targetPort: 3000
```

**Apply:**
```bash
kubectl apply -f k8s/frontend-deployment.yaml
```

---

### **Step 6: Database Migration**

#### 6.1 Migration Script

**File:** `backend/migrations/add_advanced_features.sql`

```sql
-- Add advanced feature columns
ALTER TABLE task ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';
ALTER TABLE task ADD COLUMN IF NOT EXISTS tags TEXT;
ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(50);
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_interval INTEGER;
ALTER TABLE task ADD COLUMN IF NOT EXISTS next_due_date TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS parent_task_id INTEGER REFERENCES task(id);

-- Create recurringtask table
CREATE TABLE IF NOT EXISTS recurringtask (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE REFERENCES task(id) ON DELETE CASCADE,
    pattern VARCHAR(50) NOT NULL,
    interval INTEGER NOT NULL DEFAULT 1,
    last_created_at TIMESTAMP,
    next_due_date TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create reminder table
CREATE TABLE IF NOT EXISTS reminder (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    remind_at TIMESTAMP NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### 6.2 Migration Apply

**Python Script:** `backend/scripts/check_and_fix_db.py`

```bash
# Backend pod mein run karo
kubectl exec -n todo-app -l app=todo-backend -- python3 backend/scripts/check_and_fix_db.py
```

---

### **Step 7: CORS Configuration**

#### 7.1 Backend CORS Fix

**File:** `backend/app/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

# CORS configuration
origins = [
    "http://localhost:3000",  # Local dev
    "http://148.116.94.66:3000",  # Frontend LoadBalancer IP
    "http://151.145.37.198:8000",  # Backend LoadBalancer IP
    "*"  # Development (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### **Step 8: Route Ordering Fix**

#### 8.1 Issue

FastAPI route ordering issue:
- `/{user_id}/tasks/{task_id}` route `/combined` se pehle define tha
- FastAPI "combined" ko `task_id` (integer) samajh raha tha
- Result: 422 Unprocessable Content error

#### 8.2 Fix

**File:** `backend/app/routes/tasks.py`

**Before (Wrong Order):**
```python
@router.get("/{user_id}/tasks/{task_id}")  # ❌ Pehle
@router.get("/{user_id}/tasks/combined")    # ❌ Baad mein
```

**After (Correct Order):**
```python
@router.get("/{user_id}/tasks/search")      # ✅ Specific routes pehle
@router.get("/{user_id}/tasks/filter")
@router.get("/{user_id}/tasks/sort")
@router.get("/{user_id}/tasks/combined")
@router.get("/{user_id}/tasks/{task_id}")  # ✅ Parameterized route baad mein
```

**Rule:** Specific routes (literal paths) ko parameterized routes se pehle define karo.

---

### **Step 9: Verification**

#### 9.1 Pods Check

```bash
kubectl get pods -n todo-app
```

**Expected Output:**
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-xxx-xxx            1/1     Running   0          5m
todo-backend-xxx-xxx            1/1     Running   0          5m
todo-frontend-xxx-xxx           1/1     Running   0          5m
todo-frontend-xxx-xxx           1/1     Running   0          5m
```

#### 9.2 Services Check

```bash
kubectl get svc -n todo-app
```

**Expected Output:**
```
NAME            TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)
todo-backend    LoadBalancer   10.96.3.26     151.145.37.198   8000:30381/TCP
todo-frontend   LoadBalancer   10.96.93.222   148.116.94.66    3000:30381/TCP
```

#### 9.3 Application Access

- **Frontend:** http://148.116.94.66:3000
- **Backend API:** http://151.145.37.198:8000
- **Backend Docs:** http://151.145.37.198:8000/docs

---

## 🔧 Key Fixes Applied

### 1. **Architecture Mismatch Fix**
- **Issue:** Cloud Shell (ARM64) se images build ho rahe the, OKE nodes x86_64
- **Fix:** GitHub Actions use kiya (ubuntu-latest = x86_64)

### 2. **CORS Policy Fix**
- **Issue:** Frontend backend ko call nahi kar pa raha tha
- **Fix:** Backend CORS configuration mein frontend LoadBalancer IP add kiya

### 3. **Route Ordering Fix**
- **Issue:** 422 error - FastAPI "combined" ko task_id samajh raha tha
- **Fix:** Specific routes ko parameterized routes se pehle move kiya

### 4. **Response Serialization Fix**
- **Issue:** TaskResponse model validation errors
- **Fix:** Explicit TaskResponse conversion with None value handling

### 5. **Database Schema Fix**
- **Issue:** Missing columns for advanced features
- **Fix:** Migration script se columns add kiye

---

## 📊 Deployment Commands Summary

### **Initial Setup (One Time)**
```bash
# 1. OKE Connection
oci ce cluster create-kubeconfig --cluster-id <id> --region ca-montreal-1

# 2. Namespace
kubectl create namespace todo-app

# 3. Secrets
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="..." \
  --from-literal=SECRET_KEY="..." \
  --from-literal=OPENAI_API_KEY="..." \
  -n todo-app

# 4. Deployments
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

### **Regular Updates**
```bash
# Code push to GitHub → Auto build via GitHub Actions

# Manual restart (if needed)
kubectl rollout restart deployment/todo-backend -n todo-app
kubectl rollout restart deployment/todo-frontend -n todo-app

# Check status
kubectl get pods -n todo-app
kubectl get svc -n todo-app

# View logs
kubectl logs -n todo-app -l app=todo-backend --tail=50
kubectl logs -n todo-app -l app=todo-frontend --tail=50
```

---

## 🎯 Final Results

✅ **Published App URL:** http://148.116.94.66:3000  
✅ **Dashboard URL:** http://148.116.94.66:3000/dashboard  
✅ **Backend API:** http://151.145.37.198:8000  
✅ **API Documentation:** http://151.145.37.198:8000/docs  
✅ **Database:** Connected and migrated  
✅ **CI/CD:** Automated via GitHub Actions  
✅ **All Features Working:** Tasks, Search, Filter, Sort, Priorities, Tags

### 📍 URL Details

- **Main Application:** http://148.116.94.66:3000 (Root landing page)
- **Dashboard (Tasks):** http://148.116.94.66:3000/dashboard (Direct tasks page)
- **Backend API:** http://151.145.37.198:8000 (REST API endpoint)
- **API Docs:** http://151.145.37.198:8000/docs (Swagger UI)

**For Phase 5 Submission:** Use `http://148.116.94.66:3000/dashboard` as the published app URL.  

---

## 📚 Key Learnings

1. **Route Ordering:** FastAPI mein specific routes pehle, parameterized baad mein
2. **Architecture:** Build platform aur deployment platform match hona chahiye
3. **CORS:** Frontend aur backend dono ke external IPs allow karo
4. **CI/CD:** GitHub Actions se automated builds reliable hain
5. **Database:** Migration scripts se schema updates safe hain

---

## 🚀 Next Steps (Optional)

1. **Monitoring:** Prometheus + Grafana setup
2. **Logging:** ELK Stack ya CloudWatch
3. **Auto-scaling:** HPA (Horizontal Pod Autoscaler)
4. **SSL/TLS:** Cert-Manager se HTTPS enable
5. **Backup:** Database backup automation

---

**Phase 5 Complete! 🎉**

