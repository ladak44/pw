# This script reads data for particular sensor.
# param @sensor_id
# 
# airly_sensor.py @sensor_id
# 
import urllib.request
import json
import sys
from kafka import KafkaProducer


def main():
     
    n = len(sys.argv) 
    if n == 1 :
        print("Missing parameter: sensor_id.")
        exit()
    
    sensor_id = sys.argv[1]
    apikey = "JgqZOW8cEUxwyJXCJ3NscgmUPOIlAEiH"
    url = "https://airapi.airly.eu/v2/measurements/installation?installationId="+sensor_id

    print("Url:"+ url)
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/json')
    #req.add_header('Accept', 'gzip')
    req.add_header('apikey', apikey)
    try:
       with urllib.request.urlopen(req) as url:
            out_dict = json.load(url)
    except Exception as ex:
        print("Problem with access to sensor:"+sensor_id)
        print(str(ex))
        exit()

    try: 
        #producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'),compression_type='gzip')
        producer = KafkaProducer(bootstrap_servers='localhost:9092',compression_type='gzip')
    except Exception as ex:
        print("Problem with connection to broker.")
        print(str(ex))
        exit()

    try: 
        key_bytes = bytes('9941', encoding='utf-8')
        value_bytes = bytes(json.dumps(out_dict), encoding='utf-8')
        #producer.send('sensor',key_bytes,value_bytes)
        producer.send('sensor',value_bytes,key_bytes)
        #producer.send('sensor','sex1',json.dumps(out_dict))
        #producer.send('sensor',json.dumps(out_dict))
        producer.flush()
    except Exception as ex:
        print("Exception in sending message.")
        print(str(ex))
        exit()

    #print(json.dumps(out_dict,indent = 1))

if __name__ == '__main__':
    main()

