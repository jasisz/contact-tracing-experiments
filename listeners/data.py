from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from bluetooth.discovery.data import Encounter


@dataclass(frozen=True)
class Read:
    time: datetime
    rssi: int


@dataclass(frozen=True)
class Device:
    AVERAGE_RSSI_READS = 5

    key: str
    service_data: str
    reads: List[Read]

    @property
    def last_time(self) -> Optional[datetime.time]:
        if not self.reads:
            return None
        return self.reads[-1].time

    @property
    def last_average_rssi(self) -> Optional[int]:
        if not self.reads:
            return None
        last_rssis = [r.rssi for r in self.reads[-self.AVERAGE_RSSI_READS:]]
        return int(sum(last_rssis) / len(last_rssis))

    @property
    def first_average_rssi(self) -> Optional[int]:
        if not self.reads:
            return None
        last_rssis = [r.rssi for r in self.reads[:self.AVERAGE_RSSI_READS]]
        return int(sum(last_rssis) / len(last_rssis))

    def add_encounter(self, encounter: Encounter):
        self.reads.append(Read(rssi=encounter.rssi, time=encounter.time))
