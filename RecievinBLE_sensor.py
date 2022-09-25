"""
Service Explorer
----------------

An example showing how to access and print out the services, characteristics and
descriptors of a connected GATT server.

"""

import sys
import platform
import asyncio
import logging
import time
from bleak import BleakClient, BleakScanner
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def create_msg(json_msg):
    dt = datetime.now()
    json_msg["Timestamp"] = str(dt)

    return json_msg


async def scanner():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        if d.name == "Arduino":
            data={}
            async with BleakClient(d.address) as client:
                client.connect()
                logger.info(f"Connected: {client.is_connected}")

                for service in client.services:
                    logger.info(f"[Service] {service}")
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                                logger.info(
                                    f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                                )

                                if(char.description != "Vendor specific"):
                                    if(char.description == "Location Name"):
                                        data["Room"] = str(value.decode("utf-8"))

                                    if (char.description == "Device Name"):
                                        data["DeviceID"] = str(value.decode("utf-8"))

                                    if (char.description == "Temperature"):

                                        data["Temperature"] = float(value.decode("utf-8"))
                                    else:
                                        try:
                                            data[str(char.description)] = float(value.decode("utf-8"))
                                        except:
                                            print(char.description, ": the value is not a number")




                            except Exception as e:
                                logger.error(
                                    f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                                )

                        else:
                            value = None
                            logger.info(
                                f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                            )

                        for descriptor in char.descriptors:
                            try:
                                value = bytes(
                                    await client.read_gatt_descriptor(descriptor.handle)
                                )
                                logger.info(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                            except Exception as e:
                                logger.error(f"\t\t[Descriptor] {descriptor}) | Value: {e}")
            JSON_msg = create_msg(data)
            return JSON_msg




