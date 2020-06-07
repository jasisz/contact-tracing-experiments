from dataclasses import dataclass
from datetime import datetime

EXPOSURE_NOTIFICATIONS_UUID = "0000fd6f-0000-1000-8000-00805f9b34fb"


@dataclass(frozen=True)
class Encounter:
    device_key: str
    service_data: str
    time: datetime
    rssi: int
