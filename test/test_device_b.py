import pytest
import serial
from lcus_usb_relay_module_controller import DeviceB
from device_tests import DeviceTests

DEVICE = DeviceB

RELAY_COUNT = 2

SERIAL_PORT_CONFIG = {
	'port': 'COM3',
	'baudrate': 9600,
	'bytesize': 8,
	'timeout': 0.2,
	'stopbits': serial.STOPBITS_ONE,
	'parity': serial.PARITY_NONE,
}

@pytest.mark.usefixtures("device")
class TestDeviceB(DeviceTests):

	@pytest.mark.xfail(reason="Unable to query the number of channels with this device.")
	def test_relay_count(self, request, device):
		super().test_relay_count(request, device)

	@pytest.mark.xfail(reason='Unable to simulate a failure on this device.')
	def test_invert_closed_with_verify(self, request, device):
		super().test_invert_closed_with_verify(request, device)

