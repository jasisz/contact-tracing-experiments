from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Encounter:
    device_key: str
    service_data: str
    time: datetime
    rssi: int
