# Dapr Components

This directory contains Dapr component configurations for the Todo Chatbot application.

## Components

### 1. kafka-pubsub.yaml
Kafka Pub/Sub component for event-driven architecture.

**Configuration:**
- Update `brokers` with your Kafka broker address
- For local Minikube: `kafka:9092` (if Kafka service is named "kafka")
- For cloud: Update with your Kafka cluster endpoint

**Usage:**
```python
# Publish event
await httpx.post(
    "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events",
    json={"event_type": "created", "task_id": 1}
)
```

### 2. postgresql-state.yaml
PostgreSQL state store for conversation state and caching.

**Configuration:**
- Update `connectionString` with your Neon PostgreSQL connection string
- Format: `host=... user=... password=... dbname=... sslmode=require`

**Usage:**
```python
# Save state
await httpx.post(
    "http://localhost:3500/v1.0/state/statestore",
    json=[{"key": "conversation-123", "value": {...}}]
)
```

### 3. kubernetes-secrets.yaml
Kubernetes secrets store for secure credential management.

**Usage:**
```python
# Get secret
response = await httpx.get(
    "http://localhost:3500/v1.0/secrets/kubernetes-secrets/openai-api-key"
)
```

## Deployment

### Local (Minikube)
```bash
# Apply components
kubectl apply -f dapr/components/
```

### Cloud (Oracle OKE)
```bash
# Update connection strings and broker addresses
# Then apply
kubectl apply -f dapr/components/
```

## Notes

- Components are namespace-scoped
- Update connection strings before deployment
- For production, use proper secret management
- Kafka broker address depends on your deployment (Strimzi, Redpanda, etc.)

