# Enterprise GraphRAG Pipeline

This repository demonstrates an enterprise-grade AI architecture combining big data processing, graph databases, and autonomous LLM agents. 

It fulfills the need for large-scale data ingestion and advanced semantic reasoning by bridging **Databricks** (PySpark) with **Neo4j** (Knowledge Graph) and exposing the insights directly to AI Agents using Anthropic's **Model Context Protocol (MCP)**.

## 🏗️ Architecture

1. **Data Engineering (Databricks + PySpark):** Massive datasets (e.g., financial transactions, retail interactions) are processed on a Databricks cluster. The data is cleaned and written directly into a Neo4j Graph Database using the `neo4j-spark-connector`.
2. **Graph Enrichment (Neo4j):** Once the data is in Neo4j, relationships are mapped (e.g., `Customer -[BOUGHT_AT]-> Merchant`). We can run Graph Data Science (GDS) algorithms like PageRank or Louvain to detect fraud clusters or recommendation vectors.
3. **AI Agent Layer (MCP Server):** A Python-based FastMCP server exposes the Neo4j database to any MCP-compatible LLM (like Claude Desktop or LangChain agents). The LLM can dynamically read the graph schema and execute safe, read-only Cypher queries to answer complex business questions.

## 📂 Project Structure

* `spark_ingestion.py`: The PySpark pipeline script meant to be run on Databricks. Extracts data from Delta tables and loads nodes/relationships into Neo4j.
* `mcp_neo4j_server.py`: The Model Context Protocol (MCP) server. Provides tools to the LLM (`get_graph_schema`, `execute_read_cypher`, `find_fraud_clusters`).
* `.github/workflows/python-app.yml` (Recommended): CI/CD pipeline for automated testing.

## 🚀 How to Run

### 1. Start Neo4j
You can run Neo4j locally using Docker:
```bash
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    -e NEO4J_PLUGINS='["apoc"]' \
    neo4j:latest
```

### 2. Run the Data Pipeline
In a real environment, this runs on Databricks. To test locally:
```bash
pip install pyspark neo4j
python spark_ingestion.py
```

### 3. Start the MCP Server
To connect your LLM to the graph database:
```bash
pip install mcp
python mcp_neo4j_server.py
```
*Note: To connect Claude Desktop to this MCP server, add the script to your `claude_desktop_config.json`.*

## 🌟 Why this matters (For Recruiters/Hiring Managers)
* **Big Data Scale:** Unlike standard RAG that relies on local CSVs, this uses PySpark, proving an ability to handle terabytes of unstructured data.
* **GraphRAG vs Vector RAG:** Moving beyond simple vector similarity (FAISS), this uses a Knowledge Graph to map explicit, deterministic relationships between entities, drastically reducing LLM hallucinations.
* **Model Context Protocol (MCP):** Implements the latest open standard for AI tool-use, decoupling the database logic from the specific LLM orchestration framework.
