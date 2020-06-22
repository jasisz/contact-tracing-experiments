from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import median
from typing import List, Optional

from bluetooth.discovery.data import Encounter


@dataclass(frozen=True)
class Read:
    time: datetime
    rssi: int


@dataclass(frozen=True)
class Device:
    AVERAGE_RSSI_READS = 5
    MINIMUM_GAP_BETWEEN_ENCOUNTERS = timedelta(milliseconds=10)

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
        last_rssis = [r.rssi for r in self.reads[-self.AVERAGE_RSSI_READS :]]
        return int(sum(last_rssis) / len(last_rssis))

    @property
    def first_average_rssi(self) -> Optional[int]:
        if not self.reads:
            return None
        last_rssis = [r.rssi for r in self.reads[: self.AVERAGE_RSSI_READS]]
        return int(sum(last_rssis) / len(last_rssis))

    @property
    def time_between(self) -> int:
        times = [
            (j.time - i.time).total_seconds() * 1000
            for i, j in zip(self.reads[:-1], self.reads[1:])
        ]
        if times:
            return int(median(times))
        return 0

    @property
    def presence(self) -> timedelta:
        if not self.reads:
            return timedelta()
        first = self.reads[0]
        last = self.reads[-1]
        return last.time - first.time

    def add_encounter(self, encounter: Encounter):
        if (
            self.last_time
            and encounter.time - self.last_time < self.MINIMUM_GAP_BETWEEN_ENCOUNTERS
        ):
            # too short time between encounters is just some channel hopping issue
            return
        self.reads.append(Read(rssi=encounter.rssi, time=encounter.time))
