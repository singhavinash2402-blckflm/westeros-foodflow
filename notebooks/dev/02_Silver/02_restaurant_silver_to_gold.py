# Databricks notebook source
# MAGIC %md
# MAGIC Bronze table data profiling

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    count,
    when,
    trim,
    lower,
    upper,
    min,
    max,
    countDistinct
)

bronze = spark.table("foodflow_dev.bronze.restaurants")

bronze.show(20, truncate=False)

# COMMAND ----------

null_check = bronze.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in bronze.columns
])

null_check.show()

# COMMAND ----------

from pyspark.sql.functions import col, trim

silver_df = (
    bronze
    .select(
        trim(col("restaurant_id")).alias("restaurant_id"),
        trim(col("restaurant_name")).alias("restaurant_name"),
        trim(col("city")).alias("city"),
        trim(col("state")).alias("state"),
        trim(col("country")).alias("country"),
        trim(col("address")).alias("address"),
        trim(col("cuisine")).alias("cuisine"),
        col("opening_date"),
        trim(col("phone")).alias("phone"),
        col("rating"),
        col("_ingested_at"),
        col("_ingestion_date"),
        col("_source_file")
    )
)

silver_df.show(20, truncate=False)

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

silver_df.select(
    min("rating").alias("min_rating"),
    max("rating").alias("max_rating")
).show()

# COMMAND ----------

(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("foodflow_dev.silver.restaurants")
)

# COMMAND ----------

# MAGIC %md
# MAGIC silver delta table validation

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS row_count
# MAGIC FROM foodflow_dev.silver.restaurants;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM foodflow_dev.silver.restaurants
# MAGIC ORDER BY restaurant_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE foodflow_dev.silver.restaurants;