from os import environ
environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 pyspark-shell'
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType,StructField,StringType,ArrayType,DoubleType,IntegerType
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import time

# polaczenie z brokerem
v_broker = "ec2-34-236-190-208.compute-1.amazonaws.com:9092"
v_ckpt_loc = "/tmp/checkpoint"

spark=SparkSession.builder.appName("Structured").getOrCreate()
# odczyt strumienia z tematu
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
.add("values", ArrayType(StructType().add("name",StringType()).add("value",StringType())))
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
# Data Frame ze sparsowanymi danymi
df = raw.select(f.col("key").cast("string"),f.from_json(f.col("value").cast("string"), schema).alias("parsed_value"))
# Modyfikacja Data Frama, zmiana formatu daty
stream = df.select(f.col("key").cast("integer"),
f.concat(f.split(f.col('parsed_value.current.fromDateTime'),'T')[0],f.lit(' '),f.substring(f.split(f.col('parsed_value.current.fromDateTime'),'T')[1],0,8)).alias("fromTime"),
f.concat(f.split(f.col('parsed_value.current.tillDateTime'),'T')[0],f.lit(' '),f.substring(f.split(f.col('parsed_value.current.tillDateTime'),'T')[1],0,8)).alias("untilTime"),          
f.explode("parsed_value.current.values").alias("value")).select("key","fromTime","untilTime","value.name",f.col("value.value").cast("float"))
# Zapis strumienia do pamieci (malo danych)
stream.writeStream.queryName("dane").outputMode("append").format("memory").start()

import matplotlib.dates as mdates
dfp=spark.sql("select fromTime,value,CASE WHEN (key=9002) THEN 'Ustka' \
               WHEN (key=9941) THEN 'W-wa Rembertow' \
               ELSE 'Bielsko-Biala' END Miasto \
               from dane \
               where name='HUMIDITY' \
               and fromTime > '2021-05-22 00:00:00' \
               and fromTime < '2021-05-23 00:00:00' \
               order by fromTime").toPandas()
dfp['fromTime']=pd.to_datetime(dfp['fromTime']).round('min')
dfp['value']=dfp['value'].map(lambda x: round(x, 2))
dfpp=pd.pivot_table(dfp,index='fromTime', columns='Miasto', values='value').dropna()
ax=dfpp.plot(xticks=dfpp.index,rot=90,fontsize=5)
ax.set_xlabel('Czas')
ax.set_ylabel('Wilgotność [%]')
ax.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
