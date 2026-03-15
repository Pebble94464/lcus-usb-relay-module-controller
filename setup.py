from setuptools import setup

setup(
	name = 'lcus-usb-relay-module-controller',
	version = '0.1.0',
	author = 'Pebble94464',
	author_email = 'jsn-usb2serial@pebble.plus.com',
	license = 'MIT License',
	url='https://github.com/Pebble94464/lcus-usb-relay-module-controller',
	description=('A module for controlling a USB to serial relay board'),
	long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
	keywords = ('usb-relay lcus-1 lcus-2 lcus-4 lcus-8 '),
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: System :: Hardware :: Universal Serial Bus (USB)',
		],
	packages=['lcus_usb_relay_module_controller'],
	install_requires=['pyserial>2']
	)

