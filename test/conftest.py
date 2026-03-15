import pytest
import serial
from random import randint
from dummy_device import DummyDevice

USE_DUMMY_DEVICE = False

@pytest.fixture(scope='class')
def device(request):
	if USE_DUMMY_DEVICE == False:
		# Use a real device
		try:
			# Setup
			serial_port = serial.Serial(**request.module.SERIAL_PORT_CONFIG)
			device = request.module.DEVICE(serial_port)
			yield device
			# Teardown
			if serial_port.is_open:
				serial_port.close()
		except serial.SerialException:
			print('Failed to open serial port.')
			yield None

	else:
		# Use the dummy device
		device = DummyDevice(request.module.SERIAL_PORT_CONFIG)
		yield device

@pytest.fixture(name="ch")
def random_channel(request):
	return randint(0, request.module.RELAY_COUNT - 1)
