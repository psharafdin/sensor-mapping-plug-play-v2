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
                    print(len(msglist))
                except Exception as Argument:
                    print("the device is created in IoT hub")
                    print(Argument)
            time.sleep(1)

asyncio.run(main())
