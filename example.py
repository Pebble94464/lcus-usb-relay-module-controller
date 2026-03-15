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

import serial  # import serial from the pyserial package
from lcus_usb_relay_module_controller import Device

try:
	# Create and open a serial port...
	port = serial.Serial(
		port='COM4',		# Which port is yours on? Update as needed.
		baudrate=9600,
		bytesize=8,
		timeout=0.2,
		stopbits=serial.STOPBITS_ONE,
		parity=serial.PARITY_NONE,
	)

	# Create an instance of Device and associate it with the port...
	device = Device(port)

	# Open the first relay...
	device.open(0)

	# Check the status of the first relay...
	if device.check(0) == 1:
		print('The first relay is open.')

	# Alternatively we can set and get relay states using the indexer...
	device[1] = 1		# Open the second relay (same as device.open(1))
	if device[1] == 1:  # Check if the relay is open (same as device.check(1))
		print('The second relay is open.')

	# Query the status of all relays...
	relay_status = device.query_status()
	print(relay_status)  # [1, 1, 0, 0]

	# Close all relays...
	for ch in range(0, device.relay_count):
		device.close(ch)

except Exception as err:
	print('repr', repr(err))

finally:
	if(port.is_open == True):
		port.close()
