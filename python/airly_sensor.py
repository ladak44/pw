# Skrypt odczytujący dane z API Airly i zapisujący wynik do tematu kafki o nazwie 'sensor'.
# Skrypt wykorzystuje zewnętrzny plik parametrów o nazwie: airly_param.json w formacie:
#      
#   {
#    "broker": "...",
#    "api_key": "...",
#    "url": "..."
#   }
#    
# Wywołanie skryptu wygląda następująco:
# airly_sensor.py @sensor_id
# sensor_id - identyfikator instalacji czujnika
# Np:
# airly_sensor.py 9941
#
import urllib.request
import json
import sys
from kafka import KafkaProducer


def main():
     
    n = len(sys.argv) 
    if n == 1 :
        print("Brakujacy parameter wejsciowy: sensor_id.")
        exit()
    
    sensor_id = sys.argv[1]

    try:
        with open("airly_param.json", "r") as f:
            param_dict = json.load(f)
        print(param_dict["broker"])
    except Exception as ex:
        print("Problem z odczytem pliku parametrow: airly_param.json")
        print(str(ex))
        exit()

    v_broker = param_dict["broker"]
    v_apikey = param_dict["api_key"]
    v_url = param_dict["url"]+sensor_id

    print("Url:"+ v_url)
    req = urllib.request.Request(v_url)
    req.add_header("Accept", "application/json")
    req.add_header("apikey", v_apikey)
    try:
       with urllib.request.urlopen(req) as v_url:
            out_dict = json.load(v_url)
    except Exception as ex:
        print("Problem z dostepem do sensora:"+sensor_id)
        print(str(ex))
        exit()

    try: 
        producer = KafkaProducer(bootstrap_servers=v_broker,compression_type="gzip")
    except Exception as ex:
        print("Problem z polaczeniem do brokera: "+v_broker)
        print(str(ex))
        exit()

    try: 
        key_bytes = bytes(sensor_id, encoding="utf-8")
        value_bytes = bytes(json.dumps(out_dict), encoding="utf-8")
        producer.send("sensor",value_bytes,key_bytes)
        producer.flush()
    except Exception as ex:
        print("Problem z wyslaniem wiadomosci.")
        print(str(ex))
        exit()

if __name__ == '__main__':
    main()

