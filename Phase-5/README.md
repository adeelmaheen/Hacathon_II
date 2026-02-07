# Cloud Native Todo Chatbot with Advanced Features

A modern, cloud-native todo application with advanced features, event-driven architecture, and Kubernetes deployment capabilities.

## 🚀 Features

### Core Features
- ✅ User authentication (JWT)
- ✅ Task CRUD operations
- ✅ AI-powered chat assistant (OpenAI)
- ✅ Conversation history

### Advanced Features
- ✅ **Priority Levels**: Low, Medium, High, Urgent
- ✅ **Tags**: Categorize tasks with multiple tags
- ✅ **Due Dates**: Set and track task deadlines
- ✅ **Reminders**: Schedule notifications before due dates
- ✅ **Recurring Tasks**: Daily, weekly, monthly, yearly patterns
- ✅ **Search**: Full-text search across tasks
- ✅ **Filter**: By status, priority, tags, due dates
- ✅ **Sort**: By created date, due date, priority, title

### Architecture
- ✅ **Event-Driven**: Kafka for event streaming
- ✅ **Microservices**: Dapr-enabled services
- ✅ **Cloud Native**: Kubernetes-ready
- ✅ **CI/CD**: GitHub Actions pipeline
- ✅ **Monitoring**: Prometheus/Grafana ready

## 🚀 Deployment

### Phase 5: Oracle Cloud (OKE) Deployment

**Complete deployment guide:** See [PHASE5_DEPLOYMENT_COMPLETE.md](./PHASE5_DEPLOYMENT_COMPLETE.md)

**Quick Summary:**
- ✅ Deployed to Oracle Kubernetes Engine (OKE)
- ✅ OCI Container Registry for Docker images
- ✅ GitHub Actions CI/CD pipeline
- ✅ LoadBalancer services for external access
- ✅ Database migrations applied
- ✅ CORS configured
- ✅ Route ordering fixed

**Application URLs:**
- Frontend: http://148.116.94.66:3000
- Backend API: http://151.145.37.198:8000
- API Docs: http://151.145.37.198:8000/docs

## 📁 Project Structure

```
phase-4/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models.py       # Database models
│   │   ├── routes/         # API routes
│   │   ├── events.py       # Event publishing
│   │   └── database.py     # Database connection
│   ├── migrations/         # Database migrations
│   └── Dockerfile
│
├── frontend/               # Next.js frontend
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   ├── lib/                # Utilities
│   └── Dockerfile
│
├── helm/                   # Helm charts
│   └── todo-chatbot/
│       ├── templates/      # Kubernetes manifests
│       └── values.yaml     # Configuration
│
├── dapr/                   # Dapr components
│   ├── components/         # Pub/Sub, State, Secrets
│   └── configurations/     # Dapr configs
│
├── kafka/                  # Kafka configuration
│   └── strimzi-kafka.yaml  # Kafka cluster config
│
├── microservices/          # Microservices
│   ├── recurring-task-service/
│   └── notification-service/
│
├── k8s/                    # Kubernetes configs
│   ├── oci-ingress.yaml
│   └── monitoring.yaml
│
├── scripts/                # Deployment scripts
│   ├── setup-dapr-minikube.ps1
│   └── setup-oke.ps1
│
└── specs/                  # Specifications
    └── features/
        ├── phase5-advanced-deployment.md
        └── phase5-implementation-plan.md
```

## 🏃 Quick Start

### Prerequisites
- Docker Desktop
- Kubernetes (Minikube or cloud cluster)
- kubectl
- Helm
- Dapr CLI

### Local Development

1. **Start Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

### Deploy to Minikube

1. **Start Minikube**
   ```powershell
   minikube start
   ```

2. **Install Dapr**
   ```powershell
   dapr init -k
   ```

3. **Deploy Application**
   ```powershell
   # Build images
   docker build -t todo-backend:latest ./backend
   docker build -t todo-frontend:latest ./frontend
   
   # Load into Minikube
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   
   # Deploy with Helm
   cd helm/todo-chatbot
   helm install todo-chatbot . -n todo-app --create-namespace
   ```

4. **Port Forward**
   ```powershell
   kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
   kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app
   ```

### Deploy to Oracle Cloud OKE

See `QUICK_START_ORACLE.md` for detailed instructions.

```powershell
# 1. Create OKE cluster in Oracle Cloud Console
# 2. Run setup script
.\scripts\setup-oke.ps1 -ClusterOCID 'ocid1...'

# 3. Push images and deploy
helm install todo-chatbot helm/todo-chatbot -n todo-app
```

## 📚 Documentation

### Setup Guides
- **[QUICK_START_ORACLE.md](QUICK_START_ORACLE.md)** - Quick Oracle Cloud setup
- **[ORACLE_CLOUD_SETUP.md](ORACLE_CLOUD_SETUP.md)** - Detailed Oracle Cloud guide
- **[PHASE5_DEPLOYMENT_GUIDE.md](PHASE5_DEPLOYMENT_GUIDE.md)** - Minikube deployment
- **[PHASE5_COMPLETE.md](PHASE5_COMPLETE.md)** - Complete implementation summary

### Specifications
- **[specs/features/phase5-advanced-deployment.md](specs/features/phase5-advanced-deployment.md)** - Full specification
- **[specs/features/phase5-implementation-plan.md](specs/features/phase5-implementation-plan.md)** - Implementation plan

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Python web framework
- **SQLModel** - Database ORM
- **PostgreSQL** - Database (Neon Cloud)
- **OpenAI** - AI chat assistant
- **Dapr** - Microservices runtime

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling

### Infrastructure
- **Kubernetes** - Container orchestration
- **Helm** - Package manager
- **Dapr** - Distributed application runtime
- **Kafka** - Event streaming (Redpanda Cloud)

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Prometheus/Grafana** - Monitoring

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
DAPR_HOST=http://localhost
DAPR_HTTP_PORT=3500
```

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Helm Values

Edit `helm/todo-chatbot/values.yaml` to customize:
- Image repositories
- Replica counts
- Resource limits
- Service types

## 📊 Architecture

```
Frontend (Next.js) → Backend (FastAPI) → PostgreSQL
                          ↓
                    Dapr Pub/Sub
                          ↓
                      Kafka Topics
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
  Recurring Task    Notification    Real-time Sync
     Service          Service          Service
```

## 🧪 Testing

### Backend API
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

### Integration
- Test task creation with advanced features
- Test search, filter, sort
- Test recurring tasks
- Test reminders

## 🚢 Deployment

### Minikube (Local)
- ✅ Dapr installed
- ✅ Application deployed
- ✅ Port forwarding active

### Oracle Cloud OKE (Production)
- ⏳ Create cluster
- ⏳ Run setup script
- ⏳ Deploy application

## 📈 Monitoring

- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Fluent Bit** - Log aggregation

See `k8s/monitoring.yaml` for configuration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is part of a hackathon submission.

## 🙏 Acknowledgments

- Oracle Cloud Infrastructure
- Dapr community
- Redpanda for Kafka alternative
- Neon for PostgreSQL hosting

---

**Status:** ✅ Phase V Complete - Ready for Production

**Last Updated:** 2026-02-04
