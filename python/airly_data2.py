
# Skrypt wywołujący skrypt airly_sensor.py dla czujnikow znajdujacych sie 
# w trzech lokalizacjach:
# 1. Warszawa Rembertów - sensor: 9941
# 2. Ustka - sensor: 9002
# 3. Bielsko Biała - sensor: 39984
#
import time
import os
from datetime import datetime

v_wait_time = 1800

def call_airly_sensor():
    print("###################")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("###################")
    try:
        os.system("python3 ./airly_sensor.py 9941")
        os.system("python3 ./airly_sensor.py 39984")
        os.system("python3 ./airly_sensor.py 9002")
    except Exception as ex:
        print("Problem z wykonaniem skryptu: airly_sensor.py ") 
        print(str(ex))
        exit()
    time.sleep(v_wait_time)




while True:
    call_airly_sensor()