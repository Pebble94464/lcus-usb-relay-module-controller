# Copyright JSN, 2026 <jsn-usb2serial@pebble.plus.com>

import pytest

@pytest.mark.usefixtures('device')
class DeviceTests:

	def test_not_a_test(self):
		"""This is not a test."""
		assert True == True

	def test_instance_has_alias_for_channel(self, device):
		"""Ensure the instance has a 'channel' attribute for backwards compatibility."""
		assert hasattr(device, 'channel'), "Expected 'channel' attribute is missing."
		assert device.channel is device, "'channel' is expected to point to self."

	def test_indexer(self, device, ch):
		device[ch] = 0
		device[ch] = 1
		assert device.check(ch) == 1
		device[ch] = 0
		assert device.check(ch) == 0

	def test_indexer_value_error(self, device, ch):
		device[ch] = 0
		with pytest.raises(ValueError) as excinfo:
			device[ch] = 3
		assert 'Value must be 0 (closed) or 1 (open)' in str(excinfo.value)

	def test_indexer_out_of_range(self, device):
		with pytest.raises(IndexError) as excinfo:
			device[len(device._relay_state)]
		assert 'index out of range' in str(excinfo.value)

	def test_close_and_open(self, device, ch):
		device.close(ch)
		assert device.check(ch) == 0
		device.open(ch)
		assert device.check(ch) == 1

	def test_open_and_close(self, device, ch):
		device.open(ch)
		assert device.check(ch) == 1
		device.close(ch)
		assert device.check(ch) == 0

	def test_open_with_verify(self, request, device):
		if request.module.RELAY_COUNT >= 8:
			pytest.skip('This test can only be executed against devices with' \
			' fewer than 8 relays.')
		# We're assuming a device will always report a channel with no relay
		# attached as closed.
		ch = 7 # Channel without a relay
		device.close(ch)
		with pytest.raises(Exception) as excinfo:
			device.open(ch, verify=True)
		assert 'The open command failed.' in str(excinfo.value)

	@pytest.mark.skip(reason='Unable to test a failure.')
	def test_close_with_verify(self, request, device):
		pass

	@pytest.mark.xfail(reason='Not yet implemented.')
	def test_open_all(self, device):
		device.close_all()
		device.open_all()
		for ch in range(0, device.relay_count):
			assert device.check(ch) == 1

	@pytest.mark.xfail(reason='Not yet implemented.')
	def test_close_all(self, device):
		device.open_all()
		device.close_all()
		for ch in range(0, device.relay_count):
			assert device.check(ch) == 0

	def test_invert_open(self, device, ch):
		device.open(ch)
		device.invert(ch)
		assert device.check(ch) == 0

	def test_invert_closed(self, device, ch):
		device.close(ch)
		device.invert(ch)
		assert device.check(ch) == 1

	def test_invert_closed_with_verify(self, request, device):
		if request.module.RELAY_COUNT >= 8:
			pytest.skip('This test can only be executed against devices with' \
			' fewer than 8 relays.')
		# The test assumes a device will always report a channel with no relay
		# attached as closed.
		ch = 7 # Some channel with no relay.
		device.close(ch)
		with pytest.raises(Exception) as excinfo:
			device.invert(ch, verify=True)
		assert 'command failed' in str(excinfo.value)

	@pytest.mark.skip(reason='Unable to test a failure.')
	def test_invert_open_with_verify(self, request, device):
		pass

	def test_invert_open(self, device, ch):
		device.open(ch)
		device.invert(ch)
		assert device.check(ch) == 0

	def test_relay_count(self, request, device):
		assert device.relay_count == request.module.RELAY_COUNT

	def test_query_status(self, request, device):
		rc = request.module.RELAY_COUNT
		for ch in range(0, rc):
			if ch % 2 == 0:
				# In order to test single relay devices the first relay should be opened.
				device.open(ch)
			else:
				device.close(ch)

		# Keep a copy of _relay_state
		relay_state = device._relay_state

		# Zero _relay_state
		device._relay_state = [0] * 8

		assert device._relay_state != relay_state, \
			"relay_state should not be all zeros because relays were opened."

		# Query the device to update _relay_state
		device.query_status()

		assert device._relay_state == relay_state

