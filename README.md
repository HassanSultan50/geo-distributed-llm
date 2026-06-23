# geo-distributed-llm

A proof-of-concept **geo-distributed GPT inference system**. A GPT-2 model is **split
across two nodes** (pipeline parallelism) that each run half of the transformer stack
and communicate over **gRPC**, with **Kafka** for asynchronous messaging, **MongoDB**
for storage, and **Prometheus + Grafana** for monitoring — all deployable via **Docker
Compose** or **Kubernetes**.

> Experimental / learning project exploring how a large language model can be partitioned
> and served across distributed nodes rather than on a single machine.

## How it works

GPT-2's 12 transformer blocks are partitioned into two stages:

- **Node 1** — embeddings + transformer layers `0–5` (`GPTNode1`)
- **Node 2** — transformer layers `6–11` + final layer norm (`GPTNode2`)

A request flows through the nodes as a tensor pipeline:

```
                 ┌──────────────────────┐      ┌──────────────────────┐
 client          │  Node 1  (:50051)    │      │  Node 2  (:50052)    │
 tokenize  ──────▶  GPT-2 layers 0–5    │ ───▶ │  GPT-2 layers 6–11   │ ───▶ output
 (gRPC)          │  (gRPC GPTNode)      │ gRPC │  + final LayerNorm   │      tensor
                 └──────────┬───────────┘      └──────────────────────┘
                            │ Kafka (async)            │
                            ▼                          ▼
                     ┌─────────────┐           ┌──────────────────┐
                     │   Kafka     │           │  MongoDB (store) │
                     └─────────────┘           └──────────────────┘
                  monitored by Prometheus + Grafana
```

The gRPC contract (`proto/gpt_service.proto`) is a single `Process(GPTRequest) →
GPTResponse` call passing float tensors between stages.

## Tech stack

| Layer | Tech |
|-------|------|
| Model | GPT-2 (`transformers`, PyTorch), split into 2 pipeline stages |
| Inter-node serving | gRPC (`grpcio`, protobuf) |
| Messaging | Apache Kafka + Zookeeper |
| Storage | MongoDB |
| Orchestration | Docker Compose, Kubernetes |
| Observability | Prometheus, Grafana |

## Repository structure

```
proto/            gRPC service definition (gpt_service.proto)
models/           split_gpt_model.py — GPT-2 partitioned into GPTNode1 / GPTNode2
services/
  node_1/         server + Dockerfile for the first model stage (:50051)
  node_2/         server + Dockerfile for the second model stage (:50052)
  gpt_client.py   pipeline client: tokenize → node 1 → node 2 → output
  database_service.py
kafka_services/   Kafka producer / consumer / config
kubernetes/       deployments for nodes, kafka+zookeeper, mongodb, monitoring
monitoring/       prometheus.yml + grafana_dashboard.json
docker-compose.yaml
```

## Running locally

Prerequisites: Docker + Docker Compose (and Python 3.10+ to run the client/tests).

```bash
# 1. Start infrastructure (Kafka, Zookeeper, MongoDB, monitoring) + the two nodes
docker-compose up --build

# 2. In another shell, install client deps and run a pipeline request
pip install -r requirements.txt
python services/gpt_client.py        # sends "The AI revolution is" through both nodes
```

Or deploy to a cluster with the manifests in [`kubernetes/`](kubernetes/):

```bash
kubectl apply -f kubernetes/
```

Grafana/Prometheus configs live in [`monitoring/`](monitoring/).

## Notes & limitations

This is a learning prototype, not a production server: it uses GPT-2 for tractability,
insecure gRPC channels, and a fixed 2-stage split. It's intended to demonstrate the
**architecture** of distributed model serving — partitioning, inter-node transport,
messaging, storage, and observability — rather than to maximise throughput.
