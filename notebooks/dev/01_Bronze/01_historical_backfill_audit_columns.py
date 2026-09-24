# Databricks notebook source
# MAGIC %md
# MAGIC Assess the current state

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     SUM(CASE WHEN _batch_id IS NULL THEN 1 ELSE 0 END) AS null_batch_ids,
# MAGIC     SUM(CASE WHEN _batch_id IS NOT NULL THEN 1 ELSE 0 END) AS populated_batch_ids
# MAGIC FROM foodflow_dev.silver.restaurants;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     restaurant_id,
# MAGIC     _source_file,
# MAGIC     _ingestion_date,
# MAGIC     _batch_id
# MAGIC FROM foodflow_dev.silver.restaurants
# MAGIC WHERE _batch_id IS NULL
# MAGIC ORDER BY restaurant_id;

# COMMAND ----------

# MAGIC %md
# MAGIC migration as per migration rule

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE foodflow_dev.silver.restaurants
# MAGIC SET _batch_id = '20260923_01'
# MAGIC WHERE _batch_id IS NULL
# MAGIC   AND _source_file = 'restaurants_20262309_01.csv';

# COMMAND ----------

# MAGIC %md
# MAGIC Validate

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     _batch_id,
# MAGIC     _source_file,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM foodflow_dev.silver.restaurants
# MAGIC GROUP BY
# MAGIC     _batch_id,
# MAGIC     _source_file
# MAGIC ORDER BY
# MAGIC     _batch_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS null_batch_ids
# MAGIC FROM foodflow_dev.silver.restaurants
# MAGIC WHERE _batch_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_rows
# MAGIC FROM foodflow_dev.silver.restaurants;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     restaurant_id,
# MAGIC     rating,
# MAGIC     _batch_id,
# MAGIC     _source_file
# MAGIC FROM foodflow_dev.silver.restaurants
# MAGIC WHERE restaurant_id IN ('REST-DXB-001', 'REST-HYD-001');