# Enterprise GraphRAG Pipeline (Full-Stack Production Environment)

This repository demonstrates a production-grade, full-stack AI production environment combining big data processing, graph databases, autonomous LLM agents, and a scalable web interface. 

It bridges **Databricks** (PySpark) with **Neo4j** (Knowledge Graph), exposes the insights directly to AI Agents using Anthropic's **Model Context Protocol (MCP)**, and serves the application via a **Django REST Framework** backend and **React** frontend, fully orchestrated with **Docker** and **Kubernetes**.

## 🏗️ Production System

1. **Data Engineering (Databricks + PySpark):** Massive datasets (e.g., financial transactions, retail interactions) are processed on a Databricks cluster. The data is cleaned and written directly into a Neo4j Graph Database using the `neo4j-spark-connector`.
2. **Graph Enrichment (Neo4j):** Once the data is in Neo4j, relationships are mapped (e.g., `Customer -[BOUGHT_AT]-> Merchant`). We run Graph Data Science (GDS) algorithms like PageRank or Louvain to detect fraud clusters.
3. **AI Agent Layer (MCP Server):** A Python-based FastMCP server exposes the Neo4j database to any MCP-compatible LLM. The LLM can dynamically read the graph schema and execute safe, read-only Cypher queries.
4. **Backend API (Django):** A Django REST Framework application wraps the MCP server and Neo4j driver to expose clean API endpoints for the client application.
5. **Frontend (React):** A modern React single-page application (SPA) allows end-users to chat with the Graph-Augmented LLM Agent and visualize fraud clusters.
6. **Infrastructure (Docker & Kubernetes):** The entire stack is containerized and deployable via `docker-compose` for local development, or Kubernetes (`k8s/` manifests) for production scaling.

## 📂 Project Structure

```text
├── backend/
│   ├── Dockerfile             # Django backend container definition
│   ├── manage.py              # Django entrypoint
│   ├── mcp_neo4j_server.py    # Model Context Protocol (MCP) server
│   ├── spark_ingestion.py     # PySpark pipeline script (runs on Databricks)
│   └── requirements.txt       # Python dependencies (Django, Neo4j, MCP)
├── frontend/
│   ├── Dockerfile             # NGINX + React container definition
│   └── package.json           # Node.js dependencies
├── k8s/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── neo4j-deployment.yaml
├── docker-compose.yml         # Local orchestration
└── README.md
```

## 🚀 How to Run (Local Development)

The easiest way to spin up the entire stack locally is using Docker Compose:

```bash
docker-compose up --build
```
* **Neo4j Database**: `http://localhost:7474`
* **Django Backend API**: `http://localhost:8000`
* **React Frontend**: `http://localhost:3000`

## ☁️ How to Deploy (Kubernetes)

For production deployment, apply the Kubernetes manifests:

```bash
kubectl apply -f k8s/neo4j-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```



