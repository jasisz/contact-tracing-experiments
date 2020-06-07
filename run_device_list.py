from bluetooth.discovery.core_bluetooth import CoreBluetoothDiscovery
from bluetooth.discovery.data import EXPOSURE_NOTIFICATIONS_UUID
from listeners.display_devices import CursesEncounterListener

listener = CursesEncounterListener()
bluetooth_discovery = CoreBluetoothDiscovery(
    uuid=EXPOSURE_NOTIFICATIONS_UUID, listener=listener
)
bluetooth_discovery.start()
