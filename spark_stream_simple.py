from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

spark = (
    SparkSession.builder
        .appName("SimpleKafkaToMongo")
        .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/trafiklab.departures")
        .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

schema = (
    StructType()
        .add("operator", StringType())
        .add("line", StringType())
        .add("destination", StringType())
        .add("scheduled", StringType())
        .add("realtime", StringType())
        .add("delay_seconds", IntegerType())
)

df = (
    spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "sl_stream")
        .option("startingOffsets", "earliest")
        .load()
)

parsed = (
    df.selectExpr("CAST(value AS STRING) as json")
      .select(from_json(col("json"), schema).alias("data"))
      .select("data.*")
)

def write_to_mongo(df, epoch_id):
    if not df.rdd.isEmpty():
        (
            df.write
              .format("mongo")
              .mode("append")
              .option("uri", "mongodb://mongodb:27017/trafiklab.departures")
              .save()
        )

query = (
    parsed.writeStream
        .foreachBatch(write_to_mongo)
        .outputMode("append")
        .option("checkpointLocation", "/tmp/checkpoints/kafka_to_mongo")
        .start()
)

query.awaitTermination()
