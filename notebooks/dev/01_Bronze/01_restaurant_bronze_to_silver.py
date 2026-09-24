# Databricks notebook source
print("FoodFlow Data Engineering Project")
print("Spark version:", spark.version)

# COMMAND ----------

# MAGIC %md
# MAGIC Reading raw data, and infering schema's

# COMMAND ----------

raw_path = "/Volumes/foodflow_dev/bronze/raw_files/restaurants_20262309_01.csv"

df = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("mode", "PERMISSIVE")
    .load(raw_path)
)

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

print(f"Rows: {df.count()}")
print(f"Columns: {len(df.columns)}")

df.describe().show()

# COMMAND ----------

from pyspark.sql.functions import col, sum

null_counts = df.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in df.columns
])

display(null_counts)

# COMMAND ----------

# MAGIC %md
# MAGIC creating bronze delta table from raw data after some basic cleaning

# COMMAND ----------

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DateType,
    DoubleType
)

bronze_restaurant_schema = StructType([
    StructField("restaurant_id", StringType(), True),
    StructField("restaurant_name", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("country", StringType(), True),
    StructField("address", StringType(), True),
    StructField("cuisine", StringType(), True),
    StructField("opening_date", DateType(), True),
    StructField("phone", StringType(), True),
    StructField("rating", DoubleType(), True)
])

# COMMAND ----------

raw_path = "/Volumes/foodflow_dev/bronze/raw_files/restaurants_20262309_01.csv"

bronze_df = (
    spark.read
    .format("csv")
    .option("header", "true")
    .schema(bronze_restaurant_schema)
    .option("mode", "PERMISSIVE")
    .load(raw_path)
)

bronze_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import (
    current_timestamp,
    current_date,
    lit
)

bronze_df = (
    bronze_df
    .withColumn("_ingested_at", current_timestamp())
    .withColumn("_ingestion_date", current_date())
    .withColumn("_source_file", lit("restaurants_20262309_01.csv"))
)

# COMMAND ----------

bronze_df.printSchema()

# COMMAND ----------

(
    bronze_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("foodflow_dev.bronze.restaurants")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from foodflow_dev.bronze.restaurants limit 2

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS row_count
# MAGIC FROM foodflow_dev.bronze.restaurants;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE foodflow_dev.bronze.restaurants;

# COMMAND ----------

from pyspark.sql.functions import col, to_date
raw_path = "/Volumes/foodflow_dev/bronze/raw_files/restaurants_20262309_01.csv"

raw_string_df = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "false")
    .load(raw_path)
)

bronze_df = (
    raw_string_df
    .withColumn(
        "opening_date",
        to_date(col("opening_date"), "M/d/yyyy")
    )
    .withColumn("rating", col("rating").cast("double"))
)

# COMMAND ----------

bronze_df.select(
    "restaurant_id",
    "opening_date",
    "rating"
).show(20, truncate=False)

# COMMAND ----------

bronze_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, current_date, lit

bronze_df = (
    bronze_df
    .withColumn("_ingested_at", current_timestamp())
    .withColumn("_ingestion_date", current_date())
    .withColumn("_source_file", lit("restaurants_20262309_01.csv"))
)

# COMMAND ----------

display(bronze_df)

# COMMAND ----------

display(spark.table("foodflow_dev.silver.restaurants"))

# COMMAND ----------

spark.table("foodflow_dev.silver.restaurants").printSchema()

# COMMAND ----------

spark.sql("""
DESCRIBE DETAIL foodflow_dev.silver.restaurants
""").show(truncate=False)

# COMMAND ----------