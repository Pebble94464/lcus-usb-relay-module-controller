# Copyright JSN, 2024 <jsn-usb2serial@pebble.plus.com>
#
# This script is a demo for controlling a USB relay board using Python.
# Please feel welcome to use and adapt it as you wish.
#
# The script has been developed and tested using an LCUS-4 board,
# which has a USB to serial port chip ('CH340T') manufactured by 
# Nanjing Qinheng Microelectronics Co., Ltd. (https://www.wch-ic.com/)
# The board itself possibly manufactured by 'EC Buying'.
#
# The script should also work with other boards, such as the LCUS-1, LCUS-2 and
# LCUS-8.  If you find others that work, please let me know.
#
# Please find example code and inline comments below for a guide on usage,
# from line 90 onwards.

import serial
import time

class ChannelArray(bytearray):
	"""
	Each element in the ChannelArray represents the on/off status of a relay.
	0 = closed, 1 = open.

	Setting an item in the array automatically updates the corresponding relay.
	"""
	def __init__(self, device, count):
		self._device = device
		super().__init__(count)

	def __setitem__(self, key, value, update_relay=True):
		"""Set self[key] to value, and also update its relay."""
		if update_relay:
			self._device._set_relay(key, value)
		super().__setitem__(key, value)

class Device:
	"""
	This class represents the USB relay board.
	"""
	def __init__(self, port):
		self._delay_seconds = 0.01	# Small delay introduced to fix reliability.
		self._port = port
		self.channel = None
		self.query_relay_status()

	def _set_relay(self, key, value):
		starting_id = 0xA0  		# default value is 0xA0
		ch_number = key + 1			# channel number (base 1)
		state = int(value > 0)		# 0 = closed, 1 = open
		checksum = starting_id + ch_number + state % 0xFF
		self._port.write([starting_id, ch_number, state, checksum, 0x0d, 0xa])
		time.sleep(self._delay_seconds)

	def query_relay_status(self):
		"""
		Query the status of relays on the device, and update our internal
		channel array.

		Note the device natively uses base 1 for its channel numbering,
		whereas our channel array is using base 0.

		Returns the device's native response as a list of byte arrays.
		"""
		self._port.write([0xff,0x0d,0xa])
		time.sleep(self._delay_seconds)
		lines = []
		while True:
			bytes = self._port.readline()
			if(len(bytes) == 0):
				break
			lines.append(bytes.strip())

		relay_count = len(lines)  # We assume there's one line for every relay.

		if self.channel == None:
			self.channel = ChannelArray(self, relay_count)

		for i in range(0, relay_count):
			self.channel.__setitem__(i, lines[i].find(b'OFF') < 0, False)

		return lines







if __name__ == '__main__':
	try:
		# Create and open a serial port...
		port = serial.Serial(
			port='COM3',		# Which port is yours on? Update as needed.
			baudrate=9600,
			bytesize=8,
			timeout=2,
			stopbits=serial.STOPBITS_ONE,
			parity=serial.PARITY_NONE,
		)

		# Create an instance of Device and associate it with the port...
		device = Device(port)

		# Open the first relay...
		device.channel[0] = 1

		# Query the device's relay status directly...
		#   Note that channel numbers reported by the device are base 1.
		lines = device.query_relay_status()
		for l in lines:
			print(l.decode('ascii'))

		# Alternatively we can read values from the device.channel array...
		if device.channel[0] == 1:
			print('The first relay is open.')

		# Close all relays...
		relay_count = len(device.channel)
		for i in range(0, relay_count):
			device.channel[i] = 0

	except Exception as err:
		print('repr', repr(err))

	finally:
		if(port.is_open == True):
			port.flush()
			port.close()

