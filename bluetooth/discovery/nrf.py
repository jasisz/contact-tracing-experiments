import time
from binascii import hexlify
from datetime import datetime

from SnifferAPI import Sniffer, UART
from bluetooth.discovery.base import BluetoothDiscovery
from bluetooth.discovery.data import Encounter


class NRFBluetoothDiscovery(BluetoothDiscovery):
    UUID = "03036ffd"
    service_data = "17166ffd"

    def get_baud_rates(self, interface):
        return UART.find_sniffer_baudrates(interface)

    def get_interfaces(self):
        devices = UART.find_sniffer(write_data=False)
        return devices

    def new_packet(self, notification):
        packet = notification.msg["packet"]
        try:
            payload = hexlify(bytes(packet.blePacket.payload)).decode("utf-8")
            if self.UUID in payload:
                encounter = Encounter(
                    device_key=hexlify(bytes(packet.blePacket.advAddress[:6])).decode(
                        "utf-8"
                    ),
                    service_data=payload[
                        payload.index(self.service_data) + len(self.UUID) : -6
                    ],
                    time=datetime.now(),
                    rssi=packet.RSSI,
                )
                for listener in self.listeners:
                    listener.new_encounter(encounter=encounter)
        except Exception:
            # just in case - if we do fail here it stops processing
            pass

    def start(self) -> None:
        interface = self.get_interfaces()[0]
        baudrate = self.get_baud_rates(interface)
        sniffer = Sniffer.Sniffer(interface, baudrate["default"])
        sniffer.subscribe("NEW_BLE_PACKET", self.new_packet)
        sniffer.setAdvHopSequence([37, 38, 39])
        sniffer.start()
        sniffer.scan()

        while True:
            time.sleep(0.2)
