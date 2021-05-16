# Skrypt wywołujący skrypt airly_sensor.py dla czujnikow znajdujacych sie 
# w trzech lokalizacjach:
# 1. Warszawa Rembertów - sensor: 9941
# 2. Ustka - sensor: 9002
# 3. Bielsko Biała - sensor: 39984
#
import os
import sched
import time

def main():
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(600, 1, call_airly_sensor())
    scheduler.run()

def call_airly_sensor():
    try:
        os.system("python3 ./airly_sensor.py 9941")
        os.system("python3 ./airly_sensor.py 39984")
        os.system("python3 ./airly_sensor.py 9002")
    except Exception as ex:
        print("Problem z wykonaniem skryptu: airly_sensor.py ") 
        print(str(ex))
        exit()



if __name__ == '__main__':
    main()
