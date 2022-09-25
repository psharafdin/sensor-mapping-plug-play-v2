import sys
import json
from time import sleep
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult

#update the device twin using creating a tag with central position of the room
def map_sensor_to_room(connectionStr,DEVICE_ID,Room):
    try:
        iothub_registry_manager = IoTHubRegistryManager(connectionStr)
        f = open('RoomsPosition.json')
        data = json.load(f)
        new_tags = data['Rooms'][Room]

        twin = iothub_registry_manager.get_twin(DEVICE_ID)
        twin_patch = Twin(tags=new_tags)
        twin = iothub_registry_manager.update_twin(DEVICE_ID, twin_patch, twin.etag)

        # Add a delay to account for any latency before executing the query
        sleep(1)

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("IoT Hub Device Twin service sample stopped")


if __name__ == '__main__':
    print("Starting the Python IoT Hub Device Twin service sample...")
    print()

    map_sensor_to_room()