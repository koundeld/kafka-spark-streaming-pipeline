from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType


spark = SparkSession.builder \
    .appName("cab_data_raw_streaming_to_bigquery") \
    .getOrCreate()

topic = "taxi-rides-topic"

schema = StructType([
        StructField("driver_id", StringType()),
        StructField("event_time", StringType()),  # parse later
        StructField("pickup_borough", StringType()),
        StructField("drop_borough", StringType()),
        StructField("trip_distance", DoubleType()),
        StructField("passenger_count", IntegerType()),
        StructField("fare_amount", DoubleType()),
        StructField("payment_type", StringType())
])

raw_stream = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .option("kafka.group.id", "my-spark-streaming-group") \
        .load()

#Parse stream with schema defined
parsed_stream = raw_stream.selectExpr("CAST(value as String) as json_str") \
            .select(from_json(col("json_str"), schema).alias("data")) \
            .select("data.*") \
            .withColumn("event_time", col("event_time").cast(TimestampType()))
        

# Add hourly window column for bucketing rides hourly
with_window = parsed_stream.withColumn(
    "event_hour",
    window(col("event_time"), "1 hour").getField("start")
)

final_stream = with_window.select(
    "event_hour",
    "event_time",
    "driver_id",
    "pickup_borough",
    "drop_borough",
    "trip_distance",
    "passenger_count",
    "fare_amount",
    "payment_type"
)

# Write into BigQuery (append-only)
final_stream.writeStream \
    .format("bigquery") \
    .option("table", "<proj_id>.<dataset_name>.taxi_rides_raw") \
    .option("temporaryGcsBucket", "<gcs_bucket>") \
    .option("checkpointLocation", "checkpoints/taxi_rides_raw") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
