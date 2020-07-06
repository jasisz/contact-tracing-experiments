import click

from bluetooth.discovery.core_bluetooth import CoreBluetoothDiscovery
from bluetooth.discovery.csv import CSVDiscovery
from bluetooth.discovery.nrf import NRFBluetoothDiscovery
from listeners.display_devices import CursesDisplayDevicesListener
from listeners.link_devices import LinkDevicesListener
from listeners.log import LogListener

DISCOVERY_BACKENDS = {
    "core": CoreBluetoothDiscovery,
    "nrf": NRFBluetoothDiscovery,
    "csv": CSVDiscovery,
}

LISTENERS = {
    "list": CursesDisplayDevicesListener,
    "link": LinkDevicesListener,
}


@click.command()
@click.option(
    "--backend",
    type=click.Choice(DISCOVERY_BACKENDS.keys()),
    default="nrf",
    help="Discovery backend to be used.",
    prompt=True,
)
@click.option(
    "--listener",
    type=click.Choice(LISTENERS.keys()),
    default="list",
    help="Listener to be used.",
    prompt=True,
)
@click.option(
    "--devices_log",
    type=click.File("a"),
    default=None,
    help="File to log devices to",
    prompt=False,
)
@click.option(
    "--encounters_log",
    type=click.File("r+"),
    default=None,
    help="File to log encounters to/read from in csv discovery mode",
    prompt=False,
)
def run_discovery(backend, listener, devices_log, encounters_log):
    backend_class = DISCOVERY_BACKENDS[backend]
    listener_class = LISTENERS[listener]
    listeners = [listener_class()]

    if devices_log or encounters_log:
        listeners.append(
            LogListener(devices_log=devices_log, encounters_log=encounters_log)
        )

    if backend_class == CSVDiscovery:
        if not encounters_log:
            raise ValueError("csv discovery backend needs encounters_log to read from")
        bluetooth_discovery = backend_class(
            listeners=listeners, encounters_log=encounters_log
        )
    else:
        bluetooth_discovery = backend_class(listeners=listeners)

    try:
        bluetooth_discovery.start()
    finally:
        bluetooth_discovery.cleanup()


if __name__ == "__main__":
    run_discovery()
