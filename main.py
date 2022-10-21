import json
import time
import asyncio#
import DeviceManager
import RecievinBLE_sensor
from azure.iot.device import Message
from datetime import datetime
DeviceManager = DeviceManager
BLEsensor = RecievinBLE_sensor

async def main():
    while True:
        msglist = []

        try:
            msglist = await asyncio.wait_for(BLEsensor.scanner(), timeout=180.0)
        except Exception as e:
            print(e)

        print(type(msglist))
        if msglist is not None:
            for msg in msglist:
                try:
                    # send data to Azure IoT hub
                    await DeviceManager.send_msg(msg)

                except Exception as Argument:
                    print("the device is created in IoT hub")
                    print(Argument)
            if len(msglist) == 6:
                print("successfully transmitted all sensors data to IoTHub!")

            else:
                print("Could not connect to ", 6 - len(msglist), " sensor(s) in this iteration!")
            time.sleep(1)

asyncio.run(main())
