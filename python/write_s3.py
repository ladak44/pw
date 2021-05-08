from os import environ
environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.apache.hadoop:hadoop-aws:3.1.1 pyspark-shell'
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType,StringType,StructField,ArrayType,DoubleType

v_broker = "ec2-34-224-97-20.compute-1.amazonaws.com"
#v_broker = "192.168.99.101"
v_ckpt_loc = "/tmp/ckpt3"


spark=SparkSession.builder.appName("Structured").getOrCreate()
    
raw=spark.readStream.format("kafka")\
.option("kafka.bootstrap.servers",v_broker+":9092")\
.option("subscribe","sensor").load()

# Schemat napływających danych
schema = StructType()\
.add("current", StructType()\
.add("fromDateTime", StringType())\
.add("indexes", ArrayType(StructType().add("advice",StringType()).add("color",StringType()).add("description",StringType()).add("description",StringType()).add("name",StringType()).add("value",DoubleType())))\
.add("standards", ArrayType(StructType().add("averaging",StringType()).add("limit",StringType()).add("name",StringType()).add("percent",DoubleType()).add("pollutant",StringType())))\
.add("tillDateTime", StringType())\
.add("values", ArrayType(StructType().add("name",StringType()).add("value",DoubleType())))
)\
.add("forecast", ArrayType(StructType().add("fromDateTime",StringType())\
.add("indexes",ArrayType(StructType().add("advice",StringType()).add("advice",StringType()).add("color",StringType()).add("description",StringType()).add("value",DoubleType())) ) \
.add("standarts",ArrayType(StructType().add("averaging",StringType()).add("limit",StringType()).add("name",StringType()).add("percent",DoubleType()).add("pollutant",StringType()))) \
.add("tillDateTime", StringType())\
.add("values", ArrayType(StructType().add("name",StringType()).add("value",StringType())))\
))\
.add("history", ArrayType(StructType().add("fromDateTime",StringType())\
.add("indexes",ArrayType(StructType().add("advice",StringType()).add("advice",StringType()).add("color",StringType()).add("description",StringType()).add("value",DoubleType())) ) \
.add("standarts",ArrayType(StructType().add("averaging",StringType()).add("limit",StringType()).add("name",StringType()).add("percent",DoubleType()).add("pollutant",StringType()))) \
.add("tillDateTime", StringType())\
.add("values", ArrayType(StructType().add("name",StringType()).add("value",StringType())))\
))
# Data frame ze zparsowanymi danymi
df = raw.select(f.col("key").cast("String").cast("Integer"),f.from_json(f.col("value").cast("string"), schema).alias("parsed_value"))


stream = df.select(f.col("key"),f.col("parsed_value.current.fromDateTime").alias("fromTime"),f.col("parsed_value.current.tillDateTime")\
.alias("untilTime"),f.explode("parsed_value.current.values").alias("value")).select("key","fromTime","untilTime","value.*")

#stream.writeStream.format('json').outputMode("append").option("path","s3a://mladaks3/json/").start()
stream.writeStream.format('json').outputMode("append").option("checkpointLocation",v_ckpt_loc)\
.option("path","/tmp/data3").start().awaitTermination()
