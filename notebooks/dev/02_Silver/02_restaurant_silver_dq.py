# Databricks notebook source
# MAGIC %md
# MAGIC Silver data-quality checks

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    count,
    when,
    lit
)

silver = spark.table("foodflow_dev.silver.restaurants")

quality_checks = [
    (
        "restaurant_id_not_null",
        silver.filter(col("restaurant_id").isNull()).count() == 0
    ),
    (
        "restaurant_id_unique",
        silver.groupBy("restaurant_id")
              .count()
              .filter(col("count") > 1)
              .count() == 0
    ),
    (
        "restaurant_name_not_null",
        silver.filter(col("restaurant_name").isNull()).count() == 0
    ),
    (
        "city_not_null",
        silver.filter(col("city").isNull()).count() == 0
    ),
    (
        "country_not_null",
        silver.filter(col("country").isNull()).count() == 0
    ),
    (
        "opening_date_not_null",
        silver.filter(col("opening_date").isNull()).count() == 0
    ),
    (
        "phone_not_null",
        silver.filter(col("phone").isNull()).count() == 0
    ),
    (
        "rating_not_null",
        silver.filter(col("rating").isNull()).count() == 0
    ),
    (
        "rating_between_1_and_5",
        silver.filter(
            (col("rating") < 1) | (col("rating") > 5)
        ).count() == 0
    )
]

# COMMAND ----------

quality_results = spark.createDataFrame(
    quality_checks,
    ["check_name", "passed"]
)

quality_results.show(truncate=False)

# COMMAND ----------

all_checks_passed = all(
    result[1] for result in quality_checks
)

print(f"All Silver quality checks passed: {all_checks_passed}")