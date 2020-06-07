from datetime import datetime, timedelta

from bluetooth.discovery.data import Encounter
from listeners.data import Device
from listeners.base import EncounterListener


class LinkDevicesListener(EncounterListener):
    """
    Listener which tries to link devices based on observed facts that when MAC is changed:
     - old data broadcast stops
     - there is a visible gap in packets which simply IS NOT a multiple of usual 280ms interval
     - rssi is roughly the same
    """

    INTERVAL = 280
    THRESHOLD = 20
    RSSI_THRESHOLD = 20
    INACTIVE_DEVICE = timedelta(seconds=20)
    TOO_LONG_GAP = timedelta(seconds=20)

    def __init__(self):
        self.devices_dict = {}
        self.found_links = set()

    def link_devices(self) -> None:
        for old_device in self.devices_dict.values():
            if datetime.now() - old_device.last_time < self.INACTIVE_DEVICE:
                continue

            for device in self.devices_dict.values():
                if (device.key, old_device.key) in self.found_links:
                    continue

                first_read = device.reads[0]
                if first_read.time < old_device.last_time:
                    continue

                time_diff = first_read.time - old_device.last_time
                if time_diff > self.TOO_LONG_GAP:
                    continue

                milliseconds = time_diff.total_seconds() * 1000
                nearest_multiple = self.INTERVAL * round(milliseconds / self.INTERVAL)
                diff = abs(milliseconds - nearest_multiple)

                if (
                    diff > self.THRESHOLD
                    and abs(old_device.last_average_rssi - first_read.rssi)
                    < self.RSSI_THRESHOLD
                ):
                    self.found_links.add((device.key, old_device.key))
                    print(
                        f"{device.key} ({device.service_data}) is likely also the {old_device.key} ({old_device.service_data})"
                    )

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
