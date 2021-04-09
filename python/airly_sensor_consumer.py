import urllib.request
import json

from kafka import KafkaProducer
from kafka import KafkaConsumer


consumer = KafkaConsumer(bootstrap_servers='localhost:9092')

from kafka import KafkaConsumer

consumer = KafkaConsumer('sensor',bootstrap_servers='localhost:9092')

for msg in consumer:
    print (msg)

