from binascii import hexlify
from datetime import datetime

import objc
from Foundation import NSBundle, CBUUID
from PyObjCTools import AppHelper

from bluetooth.discovery.base import BluetoothDiscovery
from bluetooth.discovery.data import Encounter

constants = [
    ("CBCentralManagerScanOptionAllowDuplicatesKey", b"@"),
    ("CBAdvertisementDataServiceDataKey", b"@"),
]

objc.loadBundle(
    "CoreBluetooth",
    globals(),
    bundle_path=objc.pathForFramework(
        "/System/Library/Frameworks/IOBluetooth.framework/Versions/A/Frameworks/CoreBluetooth.framework"
    ),
)
CoreBluetooth = NSBundle.bundleWithIdentifier_("com.apple.CoreBluetooth")
objc.loadBundleVariables(CoreBluetooth, globals(), constants)


class CoreBluetoothDiscovery(BluetoothDiscovery):
    def start(self) -> None:
        central_manager = CBCentralManager.alloc()
        central_manager.initWithDelegate_queue_(self, None)
        AppHelper.runConsoleEventLoop()

    def centralManagerDidUpdateState_(self, manager):
        self.manager = manager
        manager.scanForPeripheralsWithServices_options_(
            [CBUUID.UUIDWithString_(self.uuid)],
            {CBCentralManagerScanOptionAllowDuplicatesKey: objc.YES},
        )

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(
        self, manager, peripheral, data, rssi
    ):
        if CBAdvertisementDataServiceDataKey not in data:
            return
        service_data = hexlify(
            data[CBAdvertisementDataServiceDataKey][CBUUID.UUIDWithString_("FD6F")]
            .bytes()
            .tobytes()
        ).decode("ascii")
        encounter = Encounter(
            device_key=peripheral.identifier(),
            service_data=service_data,
            time=datetime.now(),
            rssi=rssi,
        )
        self.listener.new_encounter(encounter=encounter)
