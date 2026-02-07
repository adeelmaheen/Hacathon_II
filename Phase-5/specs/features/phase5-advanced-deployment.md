# Phase V: Advanced Cloud Deployment Specification

## Overview
Deploy the Todo Chatbot with advanced features to Oracle Cloud (OKE) using event-driven architecture with Kafka, Dapr runtime, and CI/CD pipeline.

## Objectives

### Part A: Advanced Features Implementation
1. Implement Advanced Level features:
   - Recurring Tasks
   - Due Dates & Reminders
2. Implement Intermediate Level features:
   - Priorities
   - Tags
   - Search, Filter, Sort
3. Add event-driven architecture with Kafka
4. Implement Dapr for distributed application runtime

### Part B: Local Deployment (Minikube)
1. Deploy to Minikube with all advanced features
2. Deploy Dapr on Minikube with:
   - Pub/Sub (Kafka abstraction)
   - State Management
   - Bindings (cron for reminders)
   - Secrets Management
   - Service Invocation

### Part C: Cloud Deployment (Oracle Cloud OKE)
1. Deploy to Oracle Cloud Kubernetes Engine (OKE)
2. Deploy Dapr on OKE with full feature set
3. Use Kafka (Redpanda Cloud or Strimzi self-hosted)
4. Set up CI/CD pipeline using GitHub Actions
5. Configure monitoring and logging

## Technology Stack

### Application Layer
- **Frontend**: Next.js 16 (React 19)
- **Backend**: FastAPI (Python 3.13)
- **Database**: Neon PostgreSQL (external)
- **AI**: OpenAI GPT-4o-mini with MCP tools

### Event-Driven Architecture
- **Message Broker**: Kafka (Redpanda Cloud or Strimzi)
- **Event Processing**: Dapr Pub/Sub
- **Topics**:
  - `task-events`: All task CRUD operations
  - `reminders`: Scheduled reminder triggers
  - `task-updates`: Real-time client sync

### Distributed Runtime
- **Dapr**: Distributed Application Runtime
  - Pub/Sub component (Kafka)
  - State Store (PostgreSQL)
  - Bindings (Cron for reminders)
  - Secrets Store (Kubernetes)
  - Service Invocation

### Infrastructure
- **Local**: Minikube
- **Cloud**: Oracle Cloud Kubernetes Engine (OKE)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana (optional)
- **Logging**: Fluentd/Fluent Bit (optional)

## Advanced Features Specification

### 1. Recurring Tasks

**User Story**: As a user, I want to create tasks that repeat automatically (daily, weekly, monthly) so I don't have to recreate them.

**Requirements**:
- Support recurrence patterns: Daily, Weekly, Monthly, Custom
- When a recurring task is completed, automatically create the next occurrence
- Store recurrence configuration: `recurrence_pattern`, `recurrence_interval`, `next_due_date`
- Event-driven: Publish `task.completed` event to Kafka, Recurring Task Service consumes and creates next task

**Event Schema**:
```json
{
  "event_type": "task.completed",
  "task_id": 123,
  "user_id": "user-123",
  "recurrence_config": {
    "pattern": "daily",
    "interval": 1,
    "next_due_date": "2026-02-05T09:00:00Z"
  },
  "timestamp": "2026-02-04T09:00:00Z"
}
```

### 2. Due Dates & Reminders

**User Story**: As a user, I want to set due dates and receive reminders for my tasks.

**Requirements**:
- Add `due_date` field to tasks
- Add `reminder_time` field (when to send reminder before due date)
- When task is created/updated with due date, publish reminder event to Kafka
- Notification Service consumes reminder events and sends notifications at scheduled time
- Use Dapr Jobs API for exact-time scheduling (not cron polling)

**Event Schema**:
```json
{
  "event_type": "reminder.scheduled",
  "task_id": 123,
  "user_id": "user-123",
  "task_title": "Buy groceries",
  "due_at": "2026-02-05T17:00:00Z",
  "remind_at": "2026-02-05T16:00:00Z",
  "timestamp": "2026-02-04T10:00:00Z"
}
```

### 3. Priorities

**User Story**: As a user, I want to assign priorities to tasks to organize my work.

**Requirements**:
- Add `priority` field: `low`, `medium`, `high`, `urgent`
- Default priority: `medium`
- Visual indicators in UI (colors, icons)
- Filter and sort by priority

### 4. Tags

**User Story**: As a user, I want to tag tasks with categories for better organization.

**Requirements**:
- Add `tags` field (array of strings)
- Support multiple tags per task
- Filter tasks by tag
- Tag suggestions/autocomplete

### 5. Search, Filter, Sort

**User Story**: As a user, I want to search, filter, and sort my tasks to find what I need quickly.

**Requirements**:
- **Search**: Full-text search on task title and description
- **Filter**: By status, priority, tags, due date range
- **Sort**: By created date, due date, priority, title

## Event-Driven Architecture

### Kafka Topics

| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `task-events` | Chat API (MCP Tools) | Recurring Task Service, Audit Service | All task CRUD operations |
| `reminders` | Chat API (when due date set) | Notification Service | Scheduled reminder triggers |
| `task-updates` | Chat API | WebSocket Service | Real-time client sync |

### Event Types

**Task Events**:
- `task.created`
- `task.updated`
- `task.completed`
- `task.deleted`
- `task.recurrence_created`

**Reminder Events**:
- `reminder.scheduled`
- `reminder.triggered`
- `reminder.sent`

### Microservices Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Next.js)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Chat API      │────▶│   Kafka         │
│   + MCP Tools   │     │   Cluster       │
└────────┬────────┘     └────────┬────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────┐     ┌─────────────────┐
│   Neon DB       │     │ Recurring Task  │
│   (External)    │     │   Service       │
└─────────────────┘     └─────────────────┘
                                │
                                ▼
                         ┌─────────────────┐
                         │ Notification   │
                         │   Service      │
                         └─────────────────┘
```

## Dapr Components

### 1. Pub/Sub Component (Kafka)

**Purpose**: Abstract Kafka behind HTTP API

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-service"
```

**Usage in Code**:
```python
# Publish event via Dapr
await httpx.post(
    "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events",
    json={"event_type": "created", "task_id": 1}
)
```

### 2. State Store Component (PostgreSQL)

**Purpose**: Store conversation state, task cache

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=neon.db user=... password=... dbname=todo"
```

### 3. Secrets Component (Kubernetes)

**Purpose**: Secure API keys and credentials

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
```

### 4. Service Invocation

**Purpose**: Frontend → Backend communication with built-in retries

**Usage**:
```typescript
// Frontend calls via Dapr sidecar
fetch("http://localhost:3500/v1.0/invoke/backend-service/method/api/chat", {...})
```

### 5. Jobs API (Scheduled Reminders)

**Purpose**: Schedule exact-time reminders (not cron polling)

**Usage**:
```python
# Schedule reminder
await httpx.post(
    f"http://localhost:3500/v1.0-alpha1/jobs/reminder-task-{task_id}",
    json={
        "dueTime": remind_at.isoformat(),
        "data": {"task_id": task_id, "user_id": user_id}
    }
)
```

## Database Schema Updates

### Tasks Table Additions

```sql
ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN tags TEXT[] DEFAULT '{}';
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;
ALTER TABLE tasks ADD COLUMN reminder_time TIMESTAMP;
ALTER TABLE tasks ADD COLUMN recurrence_pattern VARCHAR(50);
ALTER TABLE tasks ADD COLUMN recurrence_interval INTEGER;
ALTER TABLE tasks ADD COLUMN next_due_date TIMESTAMP;
```

### New Tables

**Recurring Tasks**:
```sql
CREATE TABLE recurring_tasks (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    pattern VARCHAR(50),
    interval INTEGER,
    last_created_at TIMESTAMP,
    next_due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Reminders**:
```sql
CREATE TABLE reminders (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    user_id INTEGER REFERENCES users(id),
    remind_at TIMESTAMP,
    sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Oracle Cloud (OKE) Deployment

### Cluster Requirements
- **Always Free Tier**: 4 OCPUs, 24GB RAM
- **Node Pool**: 1-2 nodes (depending on free tier limits)
- **Kubernetes Version**: Latest stable (1.28+)

### Deployment Steps
1. Create OKE cluster in Oracle Cloud Console
2. Configure kubectl to connect to OKE
3. Install Dapr on OKE cluster
4. Deploy Kafka (Strimzi or Redpanda Cloud)
5. Deploy application using Helm charts
6. Configure ingress for external access
7. Set up CI/CD pipeline
8. Configure monitoring and logging

## CI/CD Pipeline (GitHub Actions)

### Workflow Stages
1. **Build**: Build Docker images
2. **Test**: Run unit and integration tests
3. **Push**: Push images to container registry
4. **Deploy**: Deploy to OKE using Helm
5. **Verify**: Health checks and smoke tests

### GitHub Actions Workflow
```yaml
name: Deploy to OKE

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build images
      - name: Push to registry
      - name: Deploy to OKE
      - name: Verify deployment
```

## Monitoring and Logging

### Monitoring
- **Metrics**: Prometheus (optional)
- **Dashboards**: Grafana (optional)
- **Health Checks**: Kubernetes liveness/readiness probes

### Logging
- **Log Aggregation**: Fluentd/Fluent Bit (optional)
- **Log Storage**: Cloud logging service or local storage

## Success Criteria

### Part A: Advanced Features
- ✅ Recurring tasks work end-to-end
- ✅ Due dates and reminders function correctly
- ✅ Priorities, tags, search, filter, sort implemented
- ✅ Events published to Kafka for all task operations
- ✅ Dapr components configured and working

### Part B: Local Deployment
- ✅ Application deployed on Minikube
- ✅ Dapr installed and configured
- ✅ Kafka running in Minikube
- ✅ All services communicating via Dapr
- ✅ Advanced features working locally

### Part C: Cloud Deployment
- ✅ Application deployed on Oracle OKE
- ✅ Dapr deployed on OKE
- ✅ Kafka configured (Redpanda Cloud or Strimzi)
- ✅ CI/CD pipeline working
- ✅ Application accessible via public URL
- ✅ Monitoring and logging configured

## Implementation Phases

1. **Phase 5.1**: Database schema updates and models
2. **Phase 5.2**: Advanced features implementation (backend)
3. **Phase 5.3**: Advanced features implementation (frontend)
4. **Phase 5.4**: Kafka integration and event publishing
5. **Phase 5.5**: Dapr integration
6. **Phase 5.6**: Microservices (Recurring Task Service, Notification Service)
7. **Phase 5.7**: Local deployment (Minikube + Dapr + Kafka)
8. **Phase 5.8**: Oracle Cloud OKE setup
9. **Phase 5.9**: Cloud deployment
10. **Phase 5.10**: CI/CD pipeline setup
11. **Phase 5.11**: Monitoring and logging

## Dependencies

### External Services
- Neon PostgreSQL database
- OpenAI API
- Oracle Cloud account (OKE)
- Redpanda Cloud (or self-hosted Kafka)

### Tools
- Dapr CLI
- kubectl
- Helm
- GitHub Actions
- Oracle Cloud CLI (optional)

## Risk Mitigation

1. **Kafka Availability**: Use Redpanda Cloud free tier as backup
2. **OKE Free Tier Limits**: Monitor resource usage, optimize if needed
3. **Dapr Complexity**: Start with basic components, add advanced features incrementally
4. **Event Ordering**: Use Kafka partitioning for task events
5. **Reminder Timing**: Use Dapr Jobs API for exact-time scheduling

## Next Steps After Phase V

- Production hardening
- Advanced monitoring (APM)
- Multi-region deployment
- Disaster recovery
- Performance optimization

