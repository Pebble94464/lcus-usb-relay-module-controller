

# Controlling a USB to serial port relay board with Python

This repository contains some example code for controlling
an LCUS USB to serial port relay board.

The code was developed and tested using an LCUS-4 board, possibly manufactured by 'EC Buying'.
It should also work with other similar boards including the LCUS-1, LCUS-2 and LCUS-8.

![LCUS-4 USB to serial port relay board](./LCUS-4.jpg)


## Installation / uninstallation

This module can be installed by downloading the project from GitHub.
Open a command prompt, navigate to the folder containing setup.py,
and type `pip install .` and then press enter.

To verify the module has been installed type `lcus-usb-relay-module-controller`

To unintall the module type `pip uninstall lcus-usb-relay-module-controller`


# Getting Started
An example script is provided below to get you up and running quickly.

example.py:
``` py
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

```

## Troubleshooting
This module has a dependency on the serial module from pyserial, which should
have installed automatically. Before submitting a support request please verify
the version info of pyserial installed on your system using the command
`pip show pyserial`.  Note there's another package available on pypi.org named
'serial' that is incompatible. Make sure you are importing the correct module.

## Changelog

0.0.2	Installation packaged created

0.0.1	Initial release
