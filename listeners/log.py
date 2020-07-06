from typing import Optional, TextIO

from bluetooth.discovery.data import Encounter
from listeners.data import Device
from listeners.base import EncounterListener


class LogListener(EncounterListener):
    """
    Listener which logs devices/encounters as they are seen to the file
    """

    def __init__(
        self, devices_log: Optional[TextIO], encounters_log: Optional[TextIO]
    ) -> None:
        self.devices_dict = {}
        self.devices_log = devices_log
        self.encounters_log = encounters_log

    def new_encounter(self, encounter: Encounter) -> None:
        if self.encounters_log:
            self.encounters_log.write(
                f"{encounter.time.isoformat()},{encounter.device_key},{encounter.service_data},{encounter.rssi}\n"
            )
            self.encounters_log.flush()

        if (encounter.device_key, encounter.service_data) in self.devices_dict:
            return

        device = Device(
            key=encounter.device_key, service_data=encounter.service_data, reads=[]
        )
        self.devices_dict[(encounter.device_key, encounter.service_data)] = device
        if self.devices_log:
            self.devices_log.write(
                f"{encounter.time.isoformat()},{device.key},{device.service_data},{encounter.rssi}\n"
            )
            self.devices_log.flush()
