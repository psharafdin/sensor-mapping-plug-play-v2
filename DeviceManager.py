import time
from msrest.exceptions import HttpOperationError
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.device.aio import IoTHubDeviceClient
import mappingSensors
from azure.iot.device import Message
import json

CONNECTION_STRING = "HostName=iot-hub-gridd-ccps-00.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=S0C1cMKlwHZlBGkgPfaYEO4m+t5+n+8YBfz57laZGNw="

# It is used for creating conn_str of devices
CONNECTION_split = CONNECTION_STRING.split(";")
# It is used to map sensor to the room using center postion of each rooms (updating device twin)
mappingSensors = mappingSensors

# Create a json msg which is compatible with Azure IoT hub
def create_msg(json_msg):
    azure_msg = Message(json.dumps(json_msg))
    azure_msg.content_encoding = "utf-8"
    azure_msg.content_type = "application/json"
    return azure_msg


async def send_msg(jSON_msg):
    conn_str = str(retreive_device_conn_str(jSON_msg))
    azure_msg = create_msg(jSON_msg)

    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a single message
    print("Sending message...")
    await device_client.send_message(azure_msg)
    print("Message successfully sent!")

    # finally, shut down the client
    await device_client.shutdown()

#retreivie connection string of devices from their device IDs
def retreive_device_conn_str(jSON_msg):
    try:
        iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        new_device = iothub_registry_manager.get_device(jSON_msg["DeviceID"])
        connection_string = new_device.authentication.symmetric_key.primary_key
        conn_str= str(CONNECTION_split[0]+ ";DeviceId=" + jSON_msg["DeviceID"] + ";SharedAccessKey=" + connection_string)
        print(conn_str)
        return conn_str
    except HttpOperationError as ex:
        # When device doesnt exist, new device should be created on IoT hub
        create_new_device(jSON_msg)


def create_new_device(jSON_msg):
    try:
        # RegistryManager
        iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        try:
            # CreateDevice - let IoT Hub assign keys
            primary_key = ""
            secondary_key = ""
            device_state = "enabled"
            new_device = iothub_registry_manager.create_device_with_sas(
                jSON_msg["DeviceID"], primary_key, secondary_key, device_state
            )

            mappingSensors.map_sensor_to_room(CONNECTION_STRING, jSON_msg["DeviceID"], jSON_msg["Room"])

        except HttpOperationError as ex:
            if ex.response.status_code == 409:
                # 409 indicates a conflict. This happens because the device already exists.
                new_device = iothub_registry_manager.get_device(jSON_msg["DeviceID"])
            else:
                raise

        print("device <" + jSON_msg["DeviceID"] + "> has primary key = " + new_device.authentication.symmetric_key.primary_key)


    except Exception as ex:
        print("Unexpected error {0}".format(ex))
    except KeyboardInterrupt:
        print("IoTHubRegistryManager sample stopped")
