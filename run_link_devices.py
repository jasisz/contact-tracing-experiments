from bluetooth.discovery.core_bluetooth import CoreBluetoothDiscovery
from bluetooth.discovery.data import EXPOSURE_NOTIFICATIONS_UUID
from listeners.link_devices import LinkDevicesListener

listener = LinkDevicesListener()
bluetooth_discovery = CoreBluetoothDiscovery(
    uuid=EXPOSURE_NOTIFICATIONS_UUID, listeners=[listener]
)

bluetooth_discovery.start()
bluetooth_discovery.cleanup()
