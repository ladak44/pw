# Tworzenie tabeli current_data w Hive
CREATE SCHEMA airly;
USE airly;

CREATE TABLE current_data (
key string,
fromTime timestamp,
untilTime timestamp,
name string,
value string
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS
INPUTFORMAT 'com.amazonaws.emr.s3select.hive.S3SelectableTextInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://airlypw/json/'
TBLPROPERTIES (
  "s3select.format" = "json"
);
