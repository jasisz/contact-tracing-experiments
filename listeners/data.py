from dataclasses import dataclass
from datetime import datetime
from typing import List

from bluetooth.discovery.data import Encounter


@dataclass(frozen=True)
class Read:
    time: datetime
    rssi: int


@dataclass(frozen=True)
class Device:
    key: str
    service_data: str
    reads: List[Read]

    @property
    def last_time(self) -> datetime.time:
        return self.reads[-1].time

    def add_encounter(self, encounter: Encounter):
        self.reads.append(Read(rssi=encounter.rssi, time=encounter.time))
