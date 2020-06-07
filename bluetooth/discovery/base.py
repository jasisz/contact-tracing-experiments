import abc

from listeners.base import EncounterListener


class BluetoothDiscovery(abc.ABC):
    def __init__(self, uuid: str, listener: EncounterListener) -> None:
        self.uuid = uuid
        self.listener = listener

    @abc.abstractmethod
    def start(self) -> None:
        pass
