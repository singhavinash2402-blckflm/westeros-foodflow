# Databricks notebook source
batch2_path = "/Volumes/foodflow_dev/bronze/raw_files/restaurants_20262309_02.csv"

batch2_raw = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(batch2_path)
)

display(batch2_raw)

# COMMAND ----------

batch2_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC Duplicate detection

# COMMAND ----------

batch2_raw.groupBy("restaurant_id").count().orderBy("restaurant_id").show()

# COMMAND ----------

from pyspark.sql import functions as F

batch2_raw.groupBy(batch2_raw.columns).count().show()

# COMMAND ----------

# MAGIC %md
# MAGIC Deduplication

# COMMAND ----------

from pyspark.sql import functions as F

batch_id = "20260924_02"

batch2_enriched = (
    batch2_raw
    .withColumn("_batch_id", F.lit(batch_id))
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_ingestion_date", F.current_date())
    .withColumn("_source_file", F.lit("restaurants_20262309_02.csv"))
)

display(batch2_enriched)

# COMMAND ----------

batch2_deduped = (
    batch2_enriched
    .dropDuplicates(["restaurant_id"])
)

display(batch2_deduped)

# COMMAND ----------

batch2_deduped.groupBy("restaurant_id").count().orderBy("restaurant_id").show()

# COMMAND ----------

assert batch2_deduped.count() == 3
assert batch2_deduped.select("restaurant_id").distinct().count() == 3

# COMMAND ----------

batch2_deduped.filter(
    F.col("restaurant_id") == "REST-DXB-001"
).select(
    "restaurant_id",
    "rating"
).show()

# COMMAND ----------

batch2_deduped.filter(
    F.col("restaurant_id") == "REST-HYD-001"
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC Alter silver delta table to include new auid columns

# COMMAND ----------

spark.sql("""
ALTER TABLE foodflow_dev.silver.restaurants
ADD COLUMNS (_batch_id STRING)
""")

# COMMAND ----------

spark.table("foodflow_dev.silver.restaurants").printSchema()

# COMMAND ----------

display(
    spark.table("foodflow_dev.silver.restaurants")
    .select(
        "restaurant_id",
        "restaurant_name",
        "rating",
        "_batch_id",
        "_source_file"
    )
    .orderBy("restaurant_id")
)

# COMMAND ----------

batch2_deduped.createOrReplaceTempView("restaurant_batch2")

# COMMAND ----------

display(
    spark.sql("""
        SELECT
            restaurant_id,
            restaurant_name,
            rating,
            _batch_id,
            _source_file
        FROM restaurant_batch2
        ORDER BY restaurant_id
    """)
)

# COMMAND ----------

spark.sql("""
MERGE INTO foodflow_dev.silver.restaurants AS target
USING restaurant_batch2 AS source
ON target.restaurant_id = source.restaurant_id

WHEN MATCHED AND NOT (
       target.restaurant_name <=> source.restaurant_name
   AND target.city            <=> source.city
   AND target.state           <=> source.state
   AND target.country         <=> source.country
   AND target.address         <=> source.address
   AND target.cuisine         <=> source.cuisine
   AND target.opening_date    <=> source.opening_date
   AND target.phone           <=> source.phone
   AND target.rating          <=> source.rating
)
THEN UPDATE SET
    target.restaurant_name = source.restaurant_name,
    target.city = source.city,
    target.state = source.state,
    target.country = source.country,
    target.address = source.address,
    target.cuisine = source.cuisine,
    target.opening_date = source.opening_date,
    target.phone = source.phone,
    target.rating = source.rating,
    target._ingested_at = source._ingested_at,
    target._ingestion_date = source._ingestion_date,
    target._source_file = source._source_file,
    target._batch_id = source._batch_id

WHEN NOT MATCHED
THEN INSERT (
    restaurant_id,
    restaurant_name,
    city,
    state,
    country,
    address,
    cuisine,
    opening_date,
    phone,
    rating,
    _ingested_at,
    _ingestion_date,
    _source_file,
    _batch_id
)
VALUES (
    source.restaurant_id,
    source.restaurant_name,
    source.city,
    source.state,
    source.country,
    source.address,
    source.cuisine,
    source.opening_date,
    source.phone,
    source.rating,
    source._ingested_at,
    source._ingestion_date,
    source._source_file,
    source._batch_id
)
""")

# COMMAND ----------

display(
    spark.table("foodflow_dev.silver.restaurants")
    .select(
        "restaurant_id",
        "restaurant_name",
        "city",
        "rating",
        "_batch_id",
        "_source_file"
    )
    .orderBy("restaurant_id")
)

# COMMAND ----------

history = spark.sql("""
DESCRIBE HISTORY foodflow_dev.silver.restaurants
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

before_count = spark.table(
    "foodflow_dev.silver.restaurants"
).count()

print(f"Current Silver row count: {before_count}")

# COMMAND ----------

spark.table("foodflow_dev.silver.restaurants") \
    .filter("restaurant_id = 'REST-DXB-001'") \
    .select("restaurant_id", "rating", "_batch_id") \
    .show()

# COMMAND ----------

after_replay_count = spark.table(
    "foodflow_dev.silver.restaurants"
).count()

print(f"Silver row count after replay: {after_replay_count}")

assert after_replay_count == before_count

# COMMAND ----------

spark.table("foodflow_dev.silver.restaurants") \
    .filter("restaurant_id = 'REST-DXB-001'") \
    .select("restaurant_id", "rating", "_batch_id") \
    .show()

# COMMAND ----------