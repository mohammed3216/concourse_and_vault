import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import concat, lit

spark = SparkSession.builder \
    .appName("ETL Employee Data") \
    .config('spark.jars', "./postgresql-42.7.3.jar") \
    .getOrCreate()

# Define the schema for the Kafka data
payload_after_schema = StructType([
    StructField("Section", StringType(), True),
    StructField("Mar 2013", StringType(), True),
    StructField("Mar 2014", StringType(), True),
    StructField("Mar 2015", StringType(), True),
    StructField("Mar 2016", StringType(), True),
    StructField("Mar 2017", StringType(), True),
    StructField("Mar 2018", StringType(), True),
    StructField("Mar 2019", StringType(), True),
    StructField("Mar 2020", StringType(), True),
    StructField("Mar 2021", StringType(), True),
    StructField("Mar 2022", StringType(), True),
    StructField("Mar 2023", StringType(), True),
    StructField("Mar 2024", StringType(), True),
    StructField("TTM", StringType(), True)
])

payload_schema = StructType([
    StructField("after", payload_after_schema, True)
])

message_schema = StructType([
    StructField("payload", payload_schema, True)
])

# Read data from Kafka
df1 = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "postgres.public.profit_loss_data") \
    .option("includeHeaders", "true") \
    .load()

print("Schema of raw Kafka data:")
df1.printSchema()

raw_df = df1.selectExpr("CAST(value AS STRING) as json_value")


print("Printing raw JSON values from Kafka:")
query1 = raw_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Parse the JSON data using the defined schema
parsed_df = raw_df.select(from_json(col("json_value"), message_schema).alias("data")) \
    .select("data.payload.after.*")

# Print the parsed data to debug
print("Printing parsed data after applying schema:")
query2 = parsed_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Perform a simple transformation
transformed_df = parsed_df.withColumn("bouns", concat(lit('rel'), col('Section')))

# Print transformed data to verify the transformation
print("Printing transformed data to verify the transformation:")
query3 = transformed_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Write transformed data to a new Kafka topic #####"CAST(id AS STRING) AS key",
query4 = transformed_df.selectExpr( "to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "new_topic") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .start()


 
# Await termination of all queries
# query.awaitTermination()

# Await termination of all queries
spark.streams.awaitAnyTermination()
