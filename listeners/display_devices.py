import curses
from typing import Iterable

from bluetooth.discovery.data import Encounter
from listeners.data import Device
from listeners.base import EncounterListener


class CursesDisplayDevicesListener(EncounterListener):
    """
    Listener which just nicely prints seen devices
    """

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.devices_dict = {}

    def print_devices(self, devices_list: Iterable[Device]) -> None:
        devices_list = sorted(devices_list, key=lambda d: d.key)
        for index, device in enumerate(devices_list):
            last_read = device.reads[-1]
            first_read = device.reads[0]
            self.stdscr.addstr(
                index,
                0,
                f"{device.key} ({device.service_data}): {last_read.rssi} (avg {device.last_average_rssi}) (last: {last_read.time}, first: {first_read.time}, reads: {len(device.reads)}, median interval: {device.time_between}, present for {device.presence})",
            )
        self.stdscr.refresh()

    def new_encounter(self, encounter: Encounter) -> None:
        try:
            device = self.devices_dict[(encounter.device_key, encounter.service_data)]
        except KeyError:
            device = Device(
                key=encounter.device_key, service_data=encounter.service_data, reads=[]
            )
            self.devices_dict[(encounter.device_key, encounter.service_data)] = device
        device.add_encounter(encounter=encounter)
        self.print_devices(self.devices_dict.values())

    def cleanup(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
