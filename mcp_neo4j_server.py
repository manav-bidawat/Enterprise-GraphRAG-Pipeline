import os
import json
from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase

# Initialize the MCP Server
mcp = FastMCP("Neo4j-Databricks-Knowledge-Graph")

# Neo4j Connection Settings (Reads from Environment)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@mcp.tool()
def get_graph_schema() -> str:
    """
    Retrieves the schema of the Neo4j Knowledge Graph. 
    Use this tool FIRST to understand what nodes, relationships, and properties exist in the database 
    before attempting to write Cypher queries.
    """
    query = """
    CALL apoc.meta.schema() YIELD value
    RETURN value
    """
    try:
        with get_driver() as driver:
            with driver.session() as session:
                result = session.run(query)
                schema = result.single()[0]
                return json.dumps(schema, indent=2)
    except Exception as e:
        return f"Error fetching schema (ensure APOC is installed): {str(e)}"

@mcp.tool()
def execute_read_cypher(cypher_query: str) -> str:
    """
    Executes a READ-ONLY Cypher query against the Neo4j Knowledge Graph.
    Use this to extract structured insights (e.g., fraud rings, customer behavior) that were 
    ingested via the Databricks PySpark pipeline.
    
    Args:
        cypher_query: The Cypher query to execute. MUST NOT contain write operations (CREATE, MERGE, DELETE).
    """
    # Basic safety check (true read-only should be enforced at the DB user level)
    forbidden = ["CREATE", "MERGE", "DELETE", "SET", "REMOVE", "DROP"]
    if any(word in cypher_query.upper() for word in forbidden):
        return "Error: This tool only allows READ-ONLY queries."
        
    try:
        with get_driver() as driver:
            with driver.session() as session:
                result = session.run(cypher_query)
                records = [record.data() for record in result]
                return json.dumps(records, indent=2)
    except Exception as e:
        return f"Query failed: {str(e)}"

@mcp.tool()
def find_fraud_clusters(customer_id: str) -> str:
    """
    High-level business tool: Finds potential fraud rings or clusters associated with a specific customer.
    This relies on the Louvain/PageRank algorithms previously run via Databricks.
    
    Args:
        customer_id: The ID of the customer to investigate.
    """
    query = """
    MATCH (c:Customer {id: $customer_id})-[:PART_OF_CLUSTER]->(cluster:FraudCluster)
    MATCH (cluster)<-[:PART_OF_CLUSTER]-(other:Customer)
    RETURN cluster.id AS ClusterID, cluster.risk_score AS RiskScore, 
           collect(other.id) AS AssociatedCustomers
    """
    try:
        with get_driver() as driver:
            with driver.session() as session:
                result = session.run(query, customer_id=customer_id)
                records = [record.data() for record in result]
                if not records:
                    return f"No fraud clusters found for customer {customer_id}."
                return json.dumps(records, indent=2)
    except Exception as e:
        return f"Query failed: {str(e)}"

if __name__ == "__main__":
    # Start the MCP server using standard input/output (for Claude Desktop / LangChain integration)
    mcp.run()
