import abc

from bluetooth.discovery.data import Encounter


class EncounterListener(abc.ABC):
    @abc.abstractmethod
    def new_encounter(self, encounter: Encounter) -> None:
        pass

    def cleanup(self):
        pass
