import click

from bluetooth.discovery.core_bluetooth import CoreBluetoothDiscovery
from bluetooth.discovery.nrf import NRFBluetoothDiscovery
from listeners.display_devices import CursesDisplayDevicesListener
from listeners.link_devices import LinkDevicesListener

DISCOVERY_BACKENDS = {
    "core": CoreBluetoothDiscovery,
    "nrf": NRFBluetoothDiscovery,
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
def run_discovery(backend, listener):
    backend_class = DISCOVERY_BACKENDS[backend]
    listener_class = LISTENERS[listener]
    bluetooth_discovery = backend_class(listeners=[listener_class()])

    bluetooth_discovery.start()
    bluetooth_discovery.cleanup()


if __name__ == "__main__":
    run_discovery()
