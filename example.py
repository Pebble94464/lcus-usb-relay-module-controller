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
# TODO: update

import serial  # import serial from the pyserial package
from lcus_usb_relay_module_controller import Device

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
