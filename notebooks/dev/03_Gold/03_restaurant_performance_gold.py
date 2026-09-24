# Databricks notebook source
# MAGIC %md
# MAGIC How are restaurants performing by city, country, and cuisine?

# COMMAND ----------

from pyspark.sql.functions import (
    count,
    avg,
    min,
    max,
    round
)

silver = spark.table("foodflow_dev.silver.restaurants")

gold_restaurant_performance = (
    silver
    .groupBy(
        "country",
        "city",
        "cuisine"
    )
    .agg(
        count("restaurant_id").alias("restaurant_count"),
        round(avg("rating"), 2).alias("average_rating"),
        min("rating").alias("minimum_rating"),
        max("rating").alias("maximum_rating")
    )
)

# COMMAND ----------

gold_restaurant_performance.orderBy(
    "country",
    "city",
    "cuisine"
).show(truncate=False)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY foodflow_dev.gold.restaurant_performance;

# COMMAND ----------

(
    gold_restaurant_performance.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("foodflow_dev.gold.restaurant_performance")
)

# COMMAND ----------

gold = spark.table("foodflow_dev.gold.restaurant_performance")

print("Row count:", gold.count())

gold.printSchema()

gold.show(truncate=False)

# COMMAND ----------

history = spark.sql("""
DESCRIBE HISTORY foodflow_dev.gold.restaurant_performance
LIMIT 5
""")

display(
    history.select(
        "version",
        "timestamp",
        "operation",
        "operationParameters",
        "operationMetrics"
    )
)

# COMMAND ----------

silver_count = spark.table(
    "foodflow_dev.silver.restaurants"
).count()

gold_count = spark.table(
    "foodflow_dev.gold.restaurant_performance"
).count()

print("Silver restaurant rows:", silver_count)
print("Gold aggregate groups:", gold_count)

# COMMAND ----------

gold = spark.table("foodflow_dev.gold.restaurant_performance")

print(
    "Silver rows:",
    silver_count
)

print(
    "Gold summed restaurant_count:",
    gold.selectExpr(
        "sum(restaurant_count) as total_restaurants"
    ).first()["total_restaurants"]
)

# COMMAND ----------