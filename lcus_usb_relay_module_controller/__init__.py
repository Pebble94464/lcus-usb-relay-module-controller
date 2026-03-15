"""
This module allows you to control a USB relay board.

Import a device class that's compatible with your specific board. The boards
currently supported are:
- EC Buying (Device, DeviceA, LegacyDevice)
- SAMIROB, SAMIORE ROBOT (DeviceB)

Support for other brands can be implemented by extending the DeviceBase class.
"""

from .DeviceA import DeviceA
from .DeviceB import DeviceB
from .LegacyDevice import Device as LegacyDevice

Device = DeviceA  # Default to the new implementation.

__all__ = ['Device', 'DeviceA', 'DeviceB', 'LegacyDevice']
