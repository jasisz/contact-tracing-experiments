import csv
import datetime
from time import sleep
from typing import List, TextIO

from bluetooth.discovery.base import BluetoothDiscovery
from bluetooth.discovery.data import Encounter
from listeners.base import EncounterListener


class CSVDiscovery(BluetoothDiscovery):
    def __init__(self, listeners: List[EncounterListener], encounters_log: TextIO):
        super().__init__(listeners=listeners)
        self.encounters_log = encounters_log

    def start(self) -> None:
        reader = csv.reader(self.encounters_log)
        for row in reader:
            encounter = Encounter(
                time=datetime.datetime.fromisoformat(row[0]),
                device_key=row[1],
                service_data=row[2],
                rssi=int(row[3]),
            )
            for listener in self.listeners:
                listener.new_encounter(encounter=encounter)

        while True:
            sleep(10)
