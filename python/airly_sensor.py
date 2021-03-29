import urllib.request
import json
from kafka import KafkaProducer
#import sys

apikey = "JgqZOW8cEUxwyJXCJ3NscgmUPOIlAEiH"
url = "https://airapi.airly.eu/v2/measurements/installation?installationId=9941"
#url = "https://airapi.airly.eu/v2/meta/indexes"
#url = "https://airapi.airly.eu/v2/measurements/"

#http = urllib3.PoolManager()
req = urllib.request.Request(url)
#req = http.request('GET',url)
req.add_header('Accept', 'application/json')
#req.add_header('Accept', 'gzip')
req.add_header('apikey', apikey)

with urllib.request.urlopen(req) as url:
    out_dict = json.load(url)

#producer = KafkaProducer(bootstrap_servers='localhost:9092')
#producer = KafkaProducer(bootstrap_servers='127.0.1.1:9092')
#producer.send('sample', b'Hello, sex sex!')
#producer.send('sample', key=b'message-two', value=b'This is Kafka-Python')

print(json.dumps(out_dict,indent = 1))
