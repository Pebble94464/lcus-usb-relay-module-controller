from .DeviceBase import DeviceBase
import time

class DeviceB(DeviceBase):
	"""
	Supported devices:

	   SAMIROB, SAMIORE ROBOT
	"""
	CLOSE = 0
	OPEN = 1
	CLOSE_WITH_FEEDBACK = 2
	OPEN_WITH_FEEDBACK = 3
	INVERT = 4
	CHECK = 5

	def __init__(self, port):
		super().__init__(port)
		self._count = None

	def _get_feedback(self, id: int):
		"""
		This function queries a device and validates the response.

		params:
			id	Channel ID. This value should be passed in so we can verify the
				correct channel was returned, and also update our internals.

		return value:
			0 = closed, 1 = open
		"""
		time.sleep(self._delay) # Wait for relay to finish activating.
		data = self._port.read(4)
		starting_id = data[0] # expected value is 0xA0
		ch_number = data[1]   # channel + 1		# channel number (base 1)
		if ch_number != id:
			raise Exception('Unexpected channel number returned.')
		state = data[2]       # Expect 0 or 1
		checksum = data[3]
		if checksum != self._checksum(starting_id, ch_number, state):
			raise Exception('Incorrect checksum.')
		self._relay_state[id] = state # May as well update our internals here
		return state

	def open_with_feedback(self, id: int) -> int:
		"""
		Opens a relay and verifies the response.

		Parameters:
			id	Channel ID

		Return value:
			1 (open)
		"""
		print('open with feedback') #-
		self._send_command(id, self.OPEN_WITH_FEEDBACK)
		time.sleep(self._delay) # Wait for relay to activate
		return self._get_feedback(id)

	def close_with_feedback(self, id: int) -> int:
		"""
		Closes a relay and verifies the response.

		Parameters:
			id	Channel ID

		Return value:
			1 (open)
		"""
		print('close with feedback') #-
		self._send_command(id, self.CLOSE_WITH_FEEDBACK)
		time.sleep(self._delay) # Wait for relay to activate
		return self._get_feedback(id) # or, return self._relay_state[id]

	def invert(self, id, verify=False):
		old_state = self._relay_state[id]
		self._send_command(id, self.INVERT)
		new_state = self._get_feedback(id)
		if verify == True:
			if new_state == old_state:
				raise Exception('The invert command failed.')
		return new_state

	def check(self, id: int) -> int:
		self._send_command(id, self.CHECK)
		return self._get_feedback(id)

	def query_status(self) -> list[int]:
		count = self._count or len(self._relay_state)
		self._relay_state = [0] * count # Reset our internal array.
		for ch in range(0, count):
			self._relay_state[ch] = self.check(ch)
		return self._relay_state[:count]
		# Note the SAMIROB board doesn't appear to provide a command for 
		# querying all channels at once (0xFF). We're unable to detect the 
		# number of channels.
