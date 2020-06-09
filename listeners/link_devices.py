from datetime import datetime, timedelta

from bluetooth.discovery.data import Encounter
from listeners.data import Device
from listeners.base import EncounterListener


class LinkDevicesListener(EncounterListener):
    """
    Listener which tries to link devices based on easily observed facts that when MAC is changed:
     - old data broadcast stops just before new one starts
     - rssi is roughly the same
    """

    RSSI_THRESHOLD = 20
    INACTIVE_DEVICE = timedelta(seconds=20)
    TOO_LONG_GAP = timedelta(seconds=20)

    def __init__(self):
        self.devices_dict = {}

    def link_devices(self) -> None:
        device_to_delete = None
        for old_device in self.devices_dict.values():
            if datetime.now() - old_device.last_time < self.INACTIVE_DEVICE:
                continue

            # we rely on fact that python dict maintains insertion order so we will always link the first new device
            for device in self.devices_dict.values():
                first_read = device.reads[0]
                if first_read.time < old_device.last_time:
                    continue

                time_diff = first_read.time - old_device.last_time
                if time_diff > self.TOO_LONG_GAP:
                    continue

                if (
                    abs(old_device.last_average_rssi - device.first_average_rssi)
                    > self.RSSI_THRESHOLD
                ):
                    continue

                device_to_delete = old_device
                print(
                    f"{datetime.now()}: {old_device.key} ({old_device.service_data}) is now {device.key} ({device.service_data}) after gap of {int(time_diff.total_seconds() * 1000)}ms"
                )
                # do no more matching on the old device as it should be removed
                break

        if device_to_delete:
            del self.devices_dict[device_to_delete.key]

    def new_encounter(self, encounter: Encounter) -> None:
        try:
            device = self.devices_dict[encounter.device_key]
        except KeyError:
            device = Device(
                key=encounter.device_key, service_data=encounter.service_data, reads=[]
            )
            self.devices_dict[encounter.device_key] = device
        device.add_encounter(encounter=encounter)
        self.link_devices()
