# contact-tracing-experiments

My random experiments regarding Contact Tracing, focused mostly on Exposure Notification by Google and Apple.

Start by installing dependencies:
```bash
pip install -r requirements.txt
```

## Quick overview

### `bluetooth`
Currently two simple discovery backends are implemented:
- `CoreBluetoothDiscovery` - working on macOS, not reliable, lots of missing packets and long gaps
- `NRFBluetoothDiscovery` - for usage with [nRF Sniffer](https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Sniffer-for-Bluetooth-LE),
    much more reliable, but requires external hardware (and flashing it with regular nRF Sniffer hex as used with Wireshark)

Code in package `SnifferAPI` is just copied Sniffer code from Nordic Semiconductor as it is (for convenience).

### `listeners`
Listeners working on top of Bluetooth discovery.
- `CursesDisplayDevicesListener` - simply displaying list of devices it sees with some stats
- `LinkDevicesListener` - PoC of linking devices based solely on discovery data and how RPI are broadcasted
- `LogListener` - special kind of logger which just logs encounters or devices to file

### `run_discovery`:
You can run any combination of backend and listener by running:
```bash
python ./run_discovery.py
```
and you will be prompted for backend and listener.

You can also specify those arguments as options. Run this to see possible usage:
```bash
python run_discovery.py --help
```

If you want to log encounters or devices to a file you do not need to specify listener directly but rather use it like:
```bash
python run_discovery.py --devices_log devices.csv --encounters_log encounters.csv
```

Multiple listeners (as code is ready for that) might be available in future.

### `exposure_keys`
Code used to decode published infection keys.

Run it like:
```bash
python ./decode_keys.py /1591142400-00001/
```
where `/1591142400-00001/` is directory with unzipped data from Exposure Notification public registry.

As an example ProteGO Safe app from Poland publishes infected keys under https://exp.safesafe.app e.g. 
https://exp.safesafe.app//1592568000-00001.zip (notice double slash as it seems to be misconfigured).