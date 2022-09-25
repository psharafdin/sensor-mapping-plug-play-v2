import json
import time
import asyncio#
import DeviceManager
import RecievinBLE_sensor
from azure.iot.device import Message
from datetime import datetime
DeviceManager = DeviceManager
BLEsensor = RecievinBLE_sensor


while(True):
        jSON_msg = None
        try:
            # Scanning BLEs to find the sensor, connect and read data
            jSON_msg = asyncio.run(BLEsensor.scanner())

        except Exception as Argument:
            print(Argument)

        print(type(jSON_msg),jSON_msg)
        if jSON_msg is not None:
            try:
                # send data to Azure IoT hub
                asyncio.run(DeviceManager.send_msg(jSON_msg))
            except Exception as Argument:
                print("the device is created in IoT hub")
                print(Argument)
        time.sleep(6)
