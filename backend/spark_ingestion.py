"""
Databricks PySpark to Neo4j Ingestion Pipeline
This script represents the 'Data Engineering' half of the project (Option 2).
It reads massive financial transaction datasets (Delta tables) on Databricks 
and ingests them into Neo4j using the neo4j-spark-connector.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    # 1. Initialize Spark Session on Databricks
    spark = SparkSession.builder \
        .appName("Databricks_Neo4j_Enrichment") \
        .getOrCreate()

    # Configuration for Neo4j Aura / Local
    neo4j_url = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "password"

    print("Loading Silver tables from Unity Catalog...")
    # Simulate loading a massive dataframe of transactions
    # In Databricks, this would be: spark.read.table("catalog.schema.transactions")
    transactions_df = spark.createDataFrame([
        ("TX1001", "CUST_A", "MERCH_1", 250.00, "2026-09-20"),
        ("TX1002", "CUST_B", "MERCH_1", 5000.00, "2026-09-20"),
        ("TX1003", "CUST_A", "MERCH_2", 15.50, "2026-09-21"),
    ], ["tx_id", "customer_id", "merchant_id", "amount", "date"])

    print("Writing Customer Nodes to Neo4j...")
    transactions_df.select("customer_id").distinct() \
        .write \
        .format("org.neo4j.spark.DataSource") \
        .mode("Append") \
        .option("url", neo4j_url) \
        .option("authentication.basic.username", neo4j_user) \
        .option("authentication.basic.password", neo4j_password) \
        .option("labels", "Customer") \
        .option("node.keys", "customer_id") \
        .save()

    print("Writing Merchant Nodes to Neo4j...")
    transactions_df.select("merchant_id").distinct() \
        .write \
        .format("org.neo4j.spark.DataSource") \
        .mode("Append") \
        .option("url", neo4j_url) \
        .option("authentication.basic.username", neo4j_user) \
        .option("authentication.basic.password", neo4j_password) \
        .option("labels", "Merchant") \
        .option("node.keys", "merchant_id") \
        .save()

    print("Writing Transaction Relationships (Customer -[BOUGHT_AT]-> Merchant)...")
    transactions_df.write \
        .format("org.neo4j.spark.DataSource") \
        .mode("Append") \
        .option("url", neo4j_url) \
        .option("authentication.basic.username", neo4j_user) \
        .option("authentication.basic.password", neo4j_password) \
        .option("relationship", "BOUGHT_AT") \
        .option("relationship.save.strategy", "keys") \
        .option("relationship.source.labels", "Customer") \
        .option("relationship.source.node.keys", "customer_id:customer_id") \
        .option("relationship.target.labels", "Merchant") \
        .option("relationship.target.node.keys", "merchant_id:merchant_id") \
        .option("relationship.properties", "tx_id,amount,date") \
        .save()

    print("Pipeline complete. Data is ready for MCP Agent querying.")

if __name__ == "__main__":
    main()
