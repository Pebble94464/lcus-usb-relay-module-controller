# Copyright JSN, 2026 <jsn-usb2serial@pebble.plus.com>

# We can only test our device classes when a real serial port is available.
# The DummyDevice class was written as a temporary hack, to allow us to
# develop the test suite without needing to connect to a real device.

# This class is only temporary here...
class DummyDevice():
	
	def __init__(self, config):
		print('Dummy device init.')
		self.config = config
		self.channel_state = 0
		self._relay_state = [0,0,0,0,0,0,0,0]

	@property
	def relay_count(self) -> int:
		"""The number of relay channels detected."""
		return 4

	def __setitem__(self, index, value):
		value = int(value)
		if value == 0:
			self.close(index)
		elif value == 1:
			self.open(index)
		else:
			raise ValueError("Value must be 0 (closed) or 1 (open)")

	def __getitem__(self, index):
		return self._relay_state[index]

	def get_port(self):
		return self.config['port']

	def open(self, channel, verify=False):
		if channel > 4 and verify == True:
			# Simulate a relay not opening.
			self.channel_state = 0
			raise Exception('The open with verify command failed.')
		self.channel_state = 1
		self._relay_state[channel] = 1

	def close(self, channel):
		self.channel_state = 0

	def check(self, channel):
		return self.channel_state

	def invert(self, channel, verify=False):
		if self.channel_state == 0 and channel > 4 and verify == True:
			# Simulate a relay not opening.
			self.channel_state = 0
			raise Exception('The open with verify command failed.')
		self.channel_state = int(not(self.channel_state))

	def query_status(self):
		self._relay_state = [1,0,1,0,0,0,0,0]

