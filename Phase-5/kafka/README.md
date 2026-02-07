# Kafka Setup for Todo Chatbot

This directory contains Kafka configuration for event-driven architecture.

## Options

### Option 1: Strimzi (Self-hosted in Kubernetes) - Recommended for Learning

**Pros:**
- Free (just compute cost)
- Full control
- Good learning experience
- Works in Minikube

**Cons:**
- More complex setup
- Requires more resources

**Setup:**
```bash
# 1. Create namespace
kubectl create namespace kafka

# 2. Install Strimzi operator
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka'

# 3. Wait for operator to be ready
kubectl wait --for=condition=Ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# 4. Deploy Kafka cluster
kubectl apply -f kafka/strimzi-kafka.yaml

# 5. Wait for Kafka to be ready
kubectl wait --for=condition=Ready kafka/taskflow-kafka -n kafka --timeout=600s

# 6. Get Kafka bootstrap server
kubectl get kafka taskflow-kafka -n kafka -o jsonpath='{.status.listeners[0].bootstrapServers}'
```

### Option 2: Redpanda Cloud (Free Tier) - Recommended for Hackathon

**Pros:**
- Free serverless tier
- Kafka-compatible
- No Zookeeper
- Easy setup
- Fast

**Setup:**
1. Sign up at https://redpanda.com/cloud
2. Create a Serverless cluster (free tier)
3. Create topics: `task-events`, `reminders`, `task-updates`
4. Copy bootstrap server URL and credentials
5. Update Dapr component with Redpanda connection details

### Option 3: Bitnami Kafka Helm Chart

**Setup:**
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka bitnami/kafka -n kafka --create-namespace
```

## Topics

1. **task-events**: All task CRUD operations
   - Partitions: 3
   - Retention: 7 days

2. **reminders**: Scheduled reminder triggers
   - Partitions: 3
   - Retention: 7 days

3. **task-updates**: Real-time client sync
   - Partitions: 3
   - Retention: 7 days

## Testing

```bash
# List topics
kubectl exec -it kafka-0 -n kafka -- bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Consume messages
kubectl exec -it kafka-0 -n kafka -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic task-events --from-beginning
```

## Dapr Integration

Once Kafka is running, update `dapr/components/kafka-pubsub.yaml` with the correct broker address:

- Strimzi: `taskflow-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092`
- Redpanda Cloud: Your cluster endpoint
- Bitnami: `kafka.kafka.svc.cluster.local:9092`

