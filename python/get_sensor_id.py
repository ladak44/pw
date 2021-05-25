# Skrypt zwracajacy identyfikator instalacji dla podanej lokalizacji: latitude i longitude
# Np: 
# get_sensor_id.py 54.3791882839 16.242646847
# Ustka: 9002
# 

import urllib.request
import json
import sys


def main():
     

    n = len(sys.argv) 
    if n != 3 :
        print("Brakujacy parametery wejsciowe.")
        exit()
    
    v_lat = sys.argv[1]
    v_long = sys.argv[2]


    try:
        with open("airly_param.json", "r") as f:
            param_dict = json.load(f)
        print(param_dict["broker"])
    except Exception as ex:
        print("Problem z odczytem pliku parametrow: airly_param.json")
        print(str(ex))
        exit()

    v_apikey = param_dict["api_key"]
    v_url = param_dict["url"] +"?lat="+ v_lat + "&lng=" + v_long

    print("Url:"+ v_url)
    req = urllib.request.Request(v_url)
    req.add_header('Accept', 'application/json')
    req.add_header('apikey', v_apikey)

    try:
       with urllib.request.urlopen(req) as url:
            out_dict = json.load(v_url)
    except Exception as ex:
        print("Problem with access to sensor:")
        print(str(ex))
        exit()

    print(json.dumps(out_dict,indent=1))

if __name__ == '__main__':
    main()

