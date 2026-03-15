import pytest
import serial
from lcus_usb_relay_module_controller import LegacyDevice

DEVICE = LegacyDevice

RELAY_COUNT = 4

SERIAL_PORT_CONFIG = {
	'port': 'COM4',
	'baudrate': 9600,
	'bytesize': 8,
	'timeout': 0.2,
	'stopbits': serial.STOPBITS_ONE,
	'parity': serial.PARITY_NONE,
}

@pytest.mark.usefixtures("device")
class TestLegacyDevice:
	pass

	# Tests specific to the legacy device can be added here.
	# Don't bother inheriting from the DeviceTests class because most of those 
	# tests depend on functionality that's not available in the legacy device.

