
from pyspark.sql.types import StructType,StringType,StructField,ArrayType,DoubleType


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
))


# parse json
df2 = raw.select(f.from_json(f.col("value").cast("string"), schema,jsonOptions).alias("parsed_value"))

# start stream
df2.select(f.col('parsed_value.current.fromDateTime').alias('fromTime'),f.col('parsed_value.current.tillDateTime')\
.alias('untilTime'),f.explode('parsed_value.current.values').alias('value'))\
.writeStream.outputMode('append').format("console").start()





