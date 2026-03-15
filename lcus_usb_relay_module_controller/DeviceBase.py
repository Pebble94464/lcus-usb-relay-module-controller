# Copyright JSN, 2026 <jsn-usb2serial@pebble.plus.com>

import serial
import time

class DeviceBase:
	"""A base class for USB relay devices.
	
	Don't instantiate this class directly. To support a specific device, derive
	a new class from it and implement the check() and query_status() methods,
	etc. See DeviceA and DeviceB for examples of how to do this.
	"""

	CLOSE = 0
	OPEN = 1

	def __init__(self, port: serial.Serial):
		print('DeviceBase init')
		self._port = port

		self._relay_state = [0] * 8
		"""Used internally to keep track of relay states."""

		self._delay = 0.1 # Seconds
		"""A minimal delay to allow time for relay activations, etc."""

		self.channel = self
		"""Deprecated. Use an indexer directly on the Device object instead, e.g. device[0] = 1"""

		self._count = None
		"""The number of relay channels detected. This is populated lazily when the relay status is queried."""

	def __del__(self):
		if self._port and self._port.is_open == True:
			self._port.close()

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

	@property
	def relay_count(self) -> int:
		"""The number of relay channels detected."""
		if self._count == None:
			self.query_status() # updates self._count
		return self._count

	def __len__(self) -> int:
		# Required for legacy support. Example code used 'relay_count = len(device.channel)'
		return self.relay_count

	def _checksum(self, *values: int) -> int:
		return sum(values) & 0xFF

	def _send_command(self, channel, op_code):
		starting_id = 0xA0  		# default value is 0xA0
		ch_number = channel + 1		# channel number (base 1)
		checksum = self._checksum(starting_id, ch_number, op_code)
		self._port.write([starting_id, ch_number, op_code, checksum])
		time.sleep(self._delay)
		self._port.flush()
		# Our internal array is updated inside the open / close functions, not here.

	def open(self, id, verify=False) -> None:
		"""Open a relay.
		
		Params:

			id (int):
				The relay channel number (base 0).

			verify (bool):			
				Setting this to True will trigger an exception if the relay 
				fails to change as expected.
		"""
		self._relay_state[id] = 1
		self._send_command(id, self.OPEN) # op_code 1 = open
		if verify == True:
			time.sleep(self._delay) # Allow time for a relay to action
			state = self.check(id)
			if state != 1:
				raise Exception('The open command failed.')

	def open_all(self,verify=False) -> None:
		raise NotImplemented
	# TODO: implement open_all and close_all.

	def close(self, id, verify=False) -> None:
		"""Close a relay.
		
		Params:

			id (int):
				The relay channel number (base 0).

			verify (bool):			
				Setting this to True will trigger an exception if the relay 
				fails to change as expected.
		"""
		self._relay_state[id] = 0
		self._send_command(id, self.CLOSE) # op_code 0 = close
		if verify == True:
			time.sleep(self._delay) # Allow time for a relay to action
			state = self.check(id)
			if state != 0:
				raise Exception('The close command failed.')

	def check(self, id: int) -> int:
		"""Query the status of a switch.
		
		Return value: 0 or 1 for open or closed.
		"""
		pass

	def query_status(self) -> list[int]:
		"""Fetches the status of all relays on a device and ensures our
		internal array mirrors the current state.

		Return value: a list of 0s and 1s representing the state of each relay.
		"""
		pass

	def invert(self, id, verify=False) -> int:
		"""Open a closed relay, or close an opened relay.
		
		Params:

			id (int):
				The relay channel number (base 0).

			verify (bool):			
				Setting this to True will trigger an exception if the relay 
				fails to change as expected.		
		"""
		pass
