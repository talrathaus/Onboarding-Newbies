import pydantic
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, udf

# --- PHASE A ---
# DRIVER RUNNING THIS
spark = SparkSession.builder.appName("ComplexLogic").getOrCreate()
lookup_table = {"A": 1.1, "B": 1.2, "C": 1.3}

# --- PHASE B ---
# DRIVER RUNNING THIS
raw_df = spark.read.parquet("s3://data/events/")
meta_df = spark.createDataFrame([("A", "Premium"), ("B", "Standard")], ["code", "type"])


# --- PHASE C ---
# PYTHON RUNNING THIS
udf("double")
def calculate_markup(price, code):
    multiplier = lookup_table.get(code, 1.0)
    return price * multiplier


# --- PHASE D ---
# EXECUTOR RUNNING THIS
joined_df = raw_df.join(meta_df, raw_df.event_code == meta_df.code)

# --- PHASE E ---
# EXECUTOR RUNNING THIS
final_df = joined_df.withColumn(
    "final_price", calculate_markup("price", "code")
).filter(col("type") == "Premium")

# --- PHASE F ---
# EXECUTOR RUNNING THIS
report = final_df.groupBy("type").agg(avg("final_price")).collect()

# --- PHASE G ---
# DRIVER RUNNING THIS
for row in report:
    print(f"Type: {row['type']}, Avg: {row['avg(final_price)']}")
