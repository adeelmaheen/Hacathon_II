# Phase V: Implementation Plan

## Overview
This document outlines the step-by-step implementation plan for Phase V: Advanced Cloud Deployment.

## Implementation Strategy

### Approach
1. **Spec-Driven Development**: Follow AGENTS.md workflow (Specify → Plan → Tasks → Implement)
2. **Incremental Development**: Build features incrementally, test at each step
3. **Local First**: Deploy to Minikube first, then cloud
4. **Event-Driven**: Implement Kafka and Dapr early for loose coupling

## Part A: Advanced Features Implementation

### Phase 5.1: Database Schema Updates

**Objective**: Update database schema to support advanced features

**Tasks**:
1. Create migration script for new columns (priority, tags, due_date, etc.)
2. Create new tables (recurring_tasks, reminders)
3. Update SQLModel models
4. Test migrations locally

**Deliverables**:
- Migration scripts
- Updated models.py
- Database schema documentation

### Phase 5.2: Backend API Updates

**Objective**: Add API endpoints for advanced features

**Tasks**:
1. Update task creation endpoint (add priority, tags, due_date)
2. Add search endpoint (full-text search)
3. Add filter endpoint (by status, priority, tags, due_date)
4. Add sort functionality
5. Add recurring task creation endpoint
6. Add reminder scheduling endpoint

**Deliverables**:
- Updated routes/tasks.py
- New routes for search/filter/sort
- API documentation updates

### Phase 5.3: Frontend UI Updates

**Objective**: Implement UI for advanced features

**Tasks**:
1. Add priority selector component
2. Add tags input component
3. Add due date picker
4. Add search bar
5. Add filter panel
6. Add sort dropdown
7. Update task card to show priority, tags, due date
8. Add recurring task creation UI

**Deliverables**:
- Updated components
- New UI components
- Responsive design

### Phase 5.4: Kafka Integration

**Objective**: Set up Kafka and publish events

**Tasks**:
1. Choose Kafka solution (Redpanda Cloud or Strimzi)
2. Set up Kafka locally (Minikube)
3. Create Kafka producer utility
4. Publish events for all task operations
5. Create event schemas
6. Test event publishing

**Deliverables**:
- Kafka setup (local)
- Event producer code
- Event schema definitions

### Phase 5.5: Dapr Integration

**Objective**: Integrate Dapr for distributed runtime

**Tasks**:
1. Install Dapr CLI
2. Initialize Dapr on Minikube
3. Create Dapr Pub/Sub component (Kafka)
4. Create Dapr State Store component (PostgreSQL)
5. Create Dapr Secrets component (Kubernetes)
6. Update backend to use Dapr APIs
7. Test Dapr integration

**Deliverables**:
- Dapr components YAML
- Updated backend code using Dapr
- Dapr configuration

### Phase 5.6: Microservices Implementation

**Objective**: Create microservices for event processing

**Tasks**:
1. Create Recurring Task Service
   - Consume task.completed events
   - Create next occurrence
   - Publish task.created event
2. Create Notification Service
   - Consume reminder.scheduled events
   - Use Dapr Jobs API for scheduling
   - Send notifications (email/push)
3. Create Audit Service (optional)
   - Consume all task events
   - Store audit log

**Deliverables**:
- Recurring Task Service
- Notification Service
- Service Dockerfiles
- Kubernetes manifests

## Part B: Local Deployment (Minikube)

### Phase 5.7: Minikube Deployment with Dapr

**Objective**: Deploy full stack to Minikube with Dapr

**Tasks**:
1. Deploy Kafka to Minikube (Strimzi or Redpanda)
2. Install Dapr on Minikube
3. Deploy Dapr components
4. Update Helm charts for Dapr sidecars
5. Deploy application services
6. Deploy microservices
7. Test end-to-end functionality

**Deliverables**:
- Updated Helm charts
- Dapr components deployed
- All services running on Minikube

## Part C: Cloud Deployment (Oracle OKE)

### Phase 5.8: Oracle Cloud Setup

**Objective**: Set up Oracle Cloud Kubernetes Engine

**Tasks**:
1. Create OKE cluster in Oracle Cloud Console
2. Configure kubectl to connect to OKE
3. Install Dapr on OKE cluster
4. Set up container registry (Oracle Container Registry or Docker Hub)
5. Configure ingress controller
6. Set up secrets in OKE

**Deliverables**:
- OKE cluster running
- kubectl configured
- Dapr installed

### Phase 5.9: Kafka on Cloud

**Objective**: Deploy Kafka to cloud

**Tasks**:
1. Choose Kafka solution:
   - Option A: Redpanda Cloud (free tier)
   - Option B: Strimzi on OKE
2. Set up Kafka cluster
3. Create topics (task-events, reminders, task-updates)
4. Configure Dapr Pub/Sub component with cloud Kafka
5. Test connectivity

**Deliverables**:
- Kafka running on cloud
- Topics created
- Dapr connected

### Phase 5.10: Application Deployment to OKE

**Objective**: Deploy application to Oracle OKE

**Tasks**:
1. Build production Docker images
2. Push images to container registry
3. Update Helm charts for cloud deployment
4. Deploy to OKE using Helm
5. Configure ingress for public access
6. Set up DNS (if needed)
7. Verify deployment

**Deliverables**:
- Application running on OKE
- Public URL accessible
- All services healthy

### Phase 5.11: CI/CD Pipeline

**Objective**: Set up automated deployment

**Tasks**:
1. Create GitHub Actions workflow
2. Configure secrets in GitHub
3. Set up build stage (Docker images)
4. Set up test stage (unit tests)
5. Set up push stage (container registry)
6. Set up deploy stage (Helm to OKE)
7. Set up verify stage (health checks)
8. Test CI/CD pipeline

**Deliverables**:
- GitHub Actions workflow
- Automated deployment working
- Documentation

### Phase 5.12: Monitoring and Logging

**Objective**: Set up observability

**Tasks**:
1. Configure Kubernetes health checks
2. Set up basic logging (kubectl logs)
3. Optional: Deploy Prometheus
4. Optional: Deploy Grafana
5. Optional: Set up log aggregation
6. Create monitoring dashboard

**Deliverables**:
- Health checks configured
- Logging working
- Optional monitoring stack

## Task Breakdown

### Database Tasks
- [ ] T-501: Create migration for priority, tags, due_date columns
- [ ] T-502: Create recurring_tasks table
- [ ] T-503: Create reminders table
- [ ] T-504: Update SQLModel models

### Backend Tasks
- [ ] T-505: Update task creation API (priority, tags, due_date)
- [ ] T-506: Implement search API
- [ ] T-507: Implement filter API
- [ ] T-508: Implement sort API
- [ ] T-509: Implement recurring task logic
- [ ] T-510: Implement reminder scheduling

### Frontend Tasks
- [ ] T-511: Create priority selector component
- [ ] T-512: Create tags input component
- [ ] T-513: Create due date picker
- [ ] T-514: Implement search UI
- [ ] T-515: Implement filter UI
- [ ] T-516: Implement sort UI
- [ ] T-517: Update task card display

### Kafka Tasks
- [ ] T-518: Set up Kafka locally (Minikube)
- [ ] T-519: Create Kafka producer utility
- [ ] T-520: Publish task.created events
- [ ] T-521: Publish task.updated events
- [ ] T-522: Publish task.completed events
- [ ] T-523: Publish reminder.scheduled events

### Dapr Tasks
- [ ] T-524: Install Dapr CLI
- [ ] T-525: Initialize Dapr on Minikube
- [ ] T-526: Create Pub/Sub component (Kafka)
- [ ] T-527: Create State Store component
- [ ] T-528: Create Secrets component
- [ ] T-529: Update backend to use Dapr Pub/Sub
- [ ] T-530: Update backend to use Dapr State
- [ ] T-531: Implement Dapr Jobs API for reminders

### Microservices Tasks
- [ ] T-532: Create Recurring Task Service
- [ ] T-533: Create Notification Service
- [ ] T-534: Create service Dockerfiles
- [ ] T-535: Create Kubernetes manifests

### Deployment Tasks
- [ ] T-536: Deploy Kafka to Minikube
- [ ] T-537: Deploy Dapr to Minikube
- [ ] T-538: Update Helm charts for Dapr
- [ ] T-539: Deploy to Minikube
- [ ] T-540: Create OKE cluster
- [ ] T-541: Install Dapr on OKE
- [ ] T-542: Deploy Kafka to cloud
- [ ] T-543: Deploy application to OKE
- [ ] T-544: Configure ingress
- [ ] T-545: Set up CI/CD pipeline
- [ ] T-546: Configure monitoring

## Dependencies

### External
- Oracle Cloud account (OKE)
- Redpanda Cloud account (or self-hosted Kafka)
- GitHub repository
- Neon PostgreSQL database
- OpenAI API key

### Tools
- Dapr CLI
- kubectl
- Helm
- Oracle Cloud CLI (optional)
- GitHub Actions

## Timeline Estimate

- Part A (Advanced Features): 15-20 hours
- Part B (Local Deployment): 5-8 hours
- Part C (Cloud Deployment): 10-15 hours

**Total**: 30-43 hours

## Success Metrics

- ✅ All advanced features working
- ✅ Events published to Kafka
- ✅ Dapr components functional
- ✅ Application deployed on Minikube
- ✅ Application deployed on Oracle OKE
- ✅ CI/CD pipeline working
- ✅ Public URL accessible
- ✅ All services healthy

