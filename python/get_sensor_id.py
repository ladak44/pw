# This script returns installation_id for partcular localisation.
# Eg: 
# Ustka: 9002,54.3791882839,16.242646847
# Bielsko Biała: 39984,49.9645716697,19.129201811

# DO THIS
# dodac parametryacje -->>> klucz
import urllib.request
import json
import sys


def main():
     
    apikey = "JgqZOW8cEUxwyJXCJ3NscgmUPOIlAEiH"
    url = "https://airapi.airly.eu/v2/installations/nearest?lat=49.9645716697&lng=19.129201811&maxDistanceKM=5" 
    
    print("Url:"+ url)
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/json')
    req.add_header('apikey', apikey)
    try:
       with urllib.request.urlopen(req) as url:
            out_dict = json.load(url)
    except Exception as ex:
        print("Problem with access to sensor:")
        print(str(ex))
        exit()

    print(json.dumps(out_dict,indent=1))

if __name__ == '__main__':
    main()

