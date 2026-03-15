import pytest
import serial
from lcus_usb_relay_module_controller import DeviceA
from device_tests import DeviceTests

DEVICE = DeviceA

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
class TestDeviceA(DeviceTests):

	# Example of how to skip or xfail a test from the base class.
	@pytest.mark.xfail(reason="Demonstration only")
	def test_not_a_test(self):
		super().test_not_a_test()


# The test below is excluded from the test class above because it conflicts 
# with a port opened by the device fixture. Keep it here!
def test_query_relay_status():
	"""Ensure the new query_relay_status method produces the same a result as 
	the legacy device."""
	from lcus_usb_relay_module_controller import LegacyDevice
	port = serial.Serial(**SERIAL_PORT_CONFIG)
	device = DeviceA(port)
	legacy_device = LegacyDevice(port)
	assert device.query_relay_status() == legacy_device.query_relay_status()
	port.close()
