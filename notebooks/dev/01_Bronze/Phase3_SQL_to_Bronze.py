# Databricks notebook source
from pyspark.sql.functions import current_timestamp, current_date, lit

jdbc_url = (
    "jdbc:sqlserver://sql-westeros-foodflow-dev.database.windows.net:1433;"
    "databaseName=westeros-foodflow;"
    "encrypt=true;"
    "trustServerCertificate=false;"
    "loginTimeout=30;"
)

connection_properties = {
    "user": "<Your_username>",
    "password": "Avika@2402word",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}
test_df = (
    spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("query", "SELECT DB_NAME() AS database_name, GETDATE() AS server_time")
        .options(**connection_properties)
        .load()
)

display(test_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Existing restaurant table schema evolution before SQL source merge

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE foodflow_dev.bronze.restaurants
# MAGIC ADD COLUMNS (
# MAGIC     created_at TIMESTAMP,
# MAGIC     updated_at TIMESTAMP,
# MAGIC     is_active BOOLEAN,
# MAGIC     _source_system STRING,
# MAGIC     _batch_id STRING
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE foodflow_dev.bronze.restaurants;

# COMMAND ----------

# MAGIC %md
# MAGIC MERGE Azure SQL restaurants into Bronze

# COMMAND ----------

from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp, current_date, lit

batch_id = "stage3a_sql_full_20260926"

restaurants_sql_df = (
    spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", "dbo.restaurants")
        .options(**connection_properties)
        .load()
)

restaurants_bronze_df = (
    restaurants_sql_df
        .withColumn("_ingested_at", current_timestamp())
        .withColumn("_ingestion_date", current_date())
        .withColumn("_source_system", lit("azure_sql"))
        .withColumn("_batch_id", lit(batch_id))
)

display(restaurants_bronze_df)

# COMMAND ----------

from delta.tables import DeltaTable

target_table = "foodflow_dev.bronze.restaurants"

target = DeltaTable.forName(spark, target_table)

(
    target.alias("t")
    .merge(
        restaurants_bronze_df.alias("s"),
        "t.restaurant_id = s.restaurant_id"
    )
    .whenMatchedUpdate(set={
        "restaurant_name": "s.restaurant_name",
        "city": "s.city",
        "state": "s.state",
        "country": "s.country",
        "address": "s.address",
        "cuisine": "s.cuisine",
        "opening_date": "s.opening_date",
        "phone": "s.phone",
        "rating": "s.rating",
        "created_at": "s.created_at",
        "updated_at": "s.updated_at",
        "is_active": "s.is_active",
        "_ingested_at": "s._ingested_at",
        "_ingestion_date": "s._ingestion_date",
        "_source_system": "s._source_system",
        "_batch_id": "s._batch_id"
    })
    .whenNotMatchedInsert(values={
        "restaurant_id": "s.restaurant_id",
        "restaurant_name": "s.restaurant_name",
        "city": "s.city",
        "state": "s.state",
        "country": "s.country",
        "address": "s.address",
        "cuisine": "s.cuisine",
        "opening_date": "s.opening_date",
        "phone": "s.phone",
        "rating": "s.rating",
        "_ingested_at": "s._ingested_at",
        "_ingestion_date": "s._ingestion_date",
        "_source_system": "s._source_system",
        "_batch_id": "s._batch_id",
        "created_at": "s.created_at",
        "updated_at": "s.updated_at",
        "is_active": "s.is_active"
    })
    .execute()
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     _source_system,
# MAGIC     _batch_id,
# MAGIC     COUNT(*) AS row_count,
# MAGIC     COUNT(DISTINCT restaurant_id) AS distinct_restaurants
# MAGIC FROM foodflow_dev.bronze.restaurants
# MAGIC GROUP BY
# MAGIC     _source_system,
# MAGIC     _batch_id
# MAGIC ORDER BY
# MAGIC     _source_system,
# MAGIC     _batch_id;

# COMMAND ----------

# MAGIC %md
# MAGIC customer table azure sql to broze load

# COMMAND ----------

customers_df = (
    spark.read
        .jdbc(
            url=jdbc_url,
            table="dbo.customers",
            properties=connection_properties
        )
)

display(customers_df)

# COMMAND ----------

batch_id = "stage3a_full_20260926"

bronze_customers_df = (
    customers_df
        .withColumn("_ingested_at", current_timestamp())
        .withColumn("_ingestion_date", current_date())
        .withColumn("_source_system", lit("azure_sql"))
        .withColumn("_source_file", lit(None).cast("string"))
        .withColumn("_batch_id", lit(batch_id))
)

display(bronze_customers_df)

# COMMAND ----------

(
    bronze_customers_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable("foodflow_dev.bronze.customers")
)

# COMMAND ----------

# MAGIC %md
# MAGIC full 8-table sql to bronze

# COMMAND ----------

# MAGIC %md
# MAGIC Azure sql tables schema validation

# COMMAND ----------

sql_tables = [
    "customers",
    "restaurants",
    "menu_items",
    "orders",
    "order_items",
    "payments",
    "delivery_partners",
    "order_status_history",
    "restaurant_reviews",
    "delivery_partner_reviews"
]

for table_name in sql_tables:
    print(f"\n===== dbo.{table_name} =====")

    df = (
        spark.read
            .format("jdbc")
            .option("url", jdbc_url)
            .option(
                "dbtable",
                f"(SELECT TOP 0 * FROM dbo.{table_name}) AS src"
            )
            .options(**connection_properties)
            .load()
    )

    df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import (
    current_timestamp,
    current_date,
    lit
)

batch_id = "stage3a_sql_full_20260926"

# ------------------------------------------------------------
# Remaining SQL tables -> Bronze Delta tables
# Full load
# ------------------------------------------------------------

tables_to_load = [
    "menu_items",
    "orders",
    "order_items",
    "payments",
    "delivery_partners",
    "order_status_history",
    "restaurant_reviews",
    "delivery_partner_reviews"
]

results = []

for table_name in tables_to_load:

    bronze_table = f"foodflow_dev.bronze.{table_name}"

    print(f"\n{'=' * 70}")
    print(f"Processing: {table_name}")
    print(f"Bronze:     {bronze_table}")

    # --------------------------------------------------------
    # 1. Safety check
    # --------------------------------------------------------

    if spark.catalog.tableExists(bronze_table):

        raise RuntimeError(
            f"STOP: Bronze table already exists: {bronze_table}. "
            "This full-load block will not overwrite an existing table."
        )

    # --------------------------------------------------------
    # 2. Read source table from Azure SQL
    # --------------------------------------------------------

    source_df = (
        spark.read
            .jdbc(
                url=jdbc_url,
                table=f"dbo.{table_name}",
                properties=connection_properties
            )
    )

    source_count = source_df.count()

    print(f"Source rows: {source_count:,}")

    # --------------------------------------------------------
    # 3. Add standardized Bronze metadata
    # --------------------------------------------------------

    incoming_df = (
        source_df
            .withColumn("_ingested_at", current_timestamp())
            .withColumn("_ingestion_date", current_date())
            .withColumn("_source_system", lit("azure_sql"))
            .withColumn("_source_file", lit(None).cast("string"))
            .withColumn("_batch_id", lit(batch_id))
    )

    # --------------------------------------------------------
    # 4. Create Bronze Delta table
    # --------------------------------------------------------

    (
        incoming_df.write
            .format("delta")
            .mode("append")
            .saveAsTable(bronze_table)
    )

    # --------------------------------------------------------
    # 5. Validate Bronze row count
    # --------------------------------------------------------

    bronze_count = spark.table(bronze_table).count()

    if source_count != bronze_count:
        raise RuntimeError(
            f"Row-count mismatch for {table_name}: "
            f"SQL={source_count}, Bronze={bronze_count}"
        )

    results.append(
        (
            table_name,
            source_count,
            bronze_count,
            "FULL_LOAD"
        )
    )

    print(f"Bronze rows after load: {bronze_count:,}")


# ------------------------------------------------------------
# Final summary
# ------------------------------------------------------------

results_df = spark.createDataFrame(
    results,
    [
        "table_name",
        "source_count",
        "bronze_count",
        "operation"
    ]
)

display(results_df)

# COMMAND ----------

tables = [
    "menu_items",
    "orders",
    "order_items",
    "payments",
    "delivery_partners",
    "order_status_history",
    "restaurant_reviews",
    "delivery_partner_reviews"
]

validation = []

for table_name in tables:
    bronze_table = f"foodflow_dev.bronze.{table_name}"

    df = spark.table(bronze_table)

    validation.append((
        table_name,
        df.count(),
        df.filter("_source_system = 'azure_sql'").count(),
        df.filter("_batch_id = 'stage3a_sql_full_20260926'").count(),
        df.filter("_source_file IS NULL").count()
    ))

validation_df = spark.createDataFrame(
    validation,
    [
        "table_name",
        "row_count",
        "azure_sql_rows",
        "batch_rows",
        "null_source_file_rows"
    ]
)

display(validation_df.orderBy("table_name"))