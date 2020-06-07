import abc
from typing import List

from listeners.base import EncounterListener


class BluetoothDiscovery(abc.ABC):
    def __init__(self, uuid: str, listeners: List[EncounterListener]) -> None:
        self.uuid = uuid
        self.listeners = listeners

    @abc.abstractmethod
    def start(self) -> None:
        pass

    def cleanup(self):
        for listener in self.listeners:
            listener.cleanup()
