from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# Create Spark session
spark = (
    SparkSession.builder
    .appName("SalesTransformation")
    .master("local[*]")
    .getOrCreate()
)


# Read CSV
sales_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/sales.csv")
)


print("Original Sales Data:")
sales_df.show()


# Transformation
transformed_df = sales_df.withColumn(
    "total_amount",
    col("quantity") * col("price")
)


print("Transformed Sales Data:")
transformed_df.show()

spark.stop()