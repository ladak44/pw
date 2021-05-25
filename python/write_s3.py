# Skrypt odczytujacy dane z tematu kafki i zapisujący do bucketu AWS S3
# Skrypt wykorzystuje zewnętrzny plik parametrów o nazwie: airly_param.json w formacie:
#      
#   {
#    "broker": "...",
#    "api_key": "...",
#    "url": "..."
#   }
#
from os import environ
environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.apache.hadoop:hadoop-aws:3.1.1 pyspark-shell'
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType,StringType,StructField,ArrayType,DoubleType
from pyspark.sql.avro import functions as a
import json

# plik checkpoint
v_ckpt_loc = "/tmp/ckpt"

def main():

    try:
        with open("airly_param.json", "r") as file:
            param_dict = json.load(file)
        print(param_dict["broker"])
    except Exception as ex:
        print("Problem z odczytem pliku parametrow: airly_param.json")
        print(str(ex))
        exit()

    v_broker = param_dict["broker"]
    v_s3_bucket = param_dict["s3_bucket"]

    spark=SparkSession.builder.appName("Structured").getOrCreate()
    
    raw=spark.readStream.format("kafka")\
    .option("kafka.bootstrap.servers",v_broker)\
    .option("startingOffsets", "earliest")\
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

    stream = df.select(f.col("key").cast("integer"),
    f.concat(f.split(f.col('parsed_value.current.fromDateTime'),'T')[0],f.lit(' '),f.substring(f.split(f.col('parsed_value.current.fromDateTime'),'T')[1],0,8)).alias("fromTime"),
    f.concat(f.split(f.col('parsed_value.current.tillDateTime'),'T')[0],f.lit(' '),f.substring(f.split(f.col('parsed_value.current.tillDateTime'),'T')[1],0,8)).alias("untilTime"),
    f.explode("parsed_value.current.values").alias("value")).select("key","fromTime","untilTime","value.name",f.col("value.value").cast("float"))
    
    # zapis w mikrobatchach
    def write_s3(batch_df, batch_id):
        batch_df.write.format('json').mode("append").option("checkpointLocation",v_ckpt_loc)\
        .option("path",v_s3_bucket).save()

    stream.writeStream.foreachBatch(write_s3).start().awaitTermination()

if __name__ == '__main__':
    main()

