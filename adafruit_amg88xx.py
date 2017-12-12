# The MIT License (MIT)
#
# Copyright (c) 2017 Dean Miller for Adafruit Industries.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`Adafruit_AMG88xx` - AMG88xx GRID-Eye IR 8x8 IR sensor
====================================================
This library supports the use of the AMG88xx in CircuitPython. This base
class is inherited by the chip-specific subclasses.
Functions are included for reading and writing registers and manipulating
datetime objects.
Author(s): Dean Miller for Adafruit Industries.
Date: June 2017
Affiliation: Adafruit Industries
Implementation Notes
--------------------
**Hardware:**
*
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards: https://github.com/adafruit/micropython/releases
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
**Notes:**
"""

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit, i2c_bits

"""
# AMG88xx default address.
AMG88xx_I2CADDR	= 0x69

AMG88xx_PCTL 	= 0x00
AMG88xx_RST 	= 0x01
AMG88xx_FPSC 	= 0x02
AMG88xx_INTC 	= 0x03
AMG88xx_STAT 	= 0x04
AMG88xx_SCLR 	= 0x05
#0x06 reserved
AMG88xx_AVE 	= 0x07
AMG88xx_INTHL 	= 0x08
AMG88xx_INTHH 	= 0x09
AMG88xx_INTLL 	= 0x0A
AMG88xx_INTLH 	= 0x0B
AMG88xx_IHYSL 	= 0x0C
AMG88xx_IHYSH 	= 0x0D
AMG88xx_TTHL 	= 0x0E
AMG88xx_TTHH 	= 0x0F

# Operating Modes
AMG88xx_NORMAL_MODE = 0x00
AMG88xx_SLEEP_MODE = 0x01
AMG88xx_STAND_BY_60 = 0x20
AMG88xx_STAND_BY_10 = 0x21

#sw resets
AMG88xx_FLAG_RESET = 0x30
AMG88xx_INITIAL_RESET = 0x3F
	
#frame rates
AMG88xx_FPS_10 = 0x00
AMG88xx_FPS_1 = 0x01
	
#int enables
AMG88xx_INT_DISABLED = 0x00
AMG88xx_INT_ENABLED = 0x01
	
#int modes
AMG88xx_DIFFERENCE = 0x00
AMG88xx_ABSOLUTE_VALUE = 0x01
"""

AMG88xx_INT_OFFSET = 0x010
AMG88xx_PIXEL_OFFSET = 0x80

AMG88xx_PIXEL_ARRAY_SIZE = 64
AMG88xx_PIXEL_TEMP_CONVERSION = .25
AMG88xx_THERMISTOR_CONVERSION = .0625

class Adafruit_AMG88xx:

	#set up the registers
	_pctl = i2c_bits.RWBits(8, 0x00, 0)
	_rst = i2c_bits.RWBits(8, 0x01, 0)
	_fps = i2c_bit.RWBit(0x02, 0)
	_inten = i2c_bit.RWBit(0x03, 0)
	_intmod = i2c_bit.RWBit(0x03, 1)

	_intf = i2c_bit.RWBit(0x04, 1)
	_ovf_irs = i2c_bit.RWBit(0x04, 2)
	_ovf_ths = i2c_bit.RWBit(0x04, 3)

	_intclr = i2c_bit.RWBit(0x05, 1)
	_ovs_clr = i2c_bit.RWBit(0x05, 2)
	_ovt_clr = i2c_bit.RWBit(0x05, 3)

	_mamod = i2c_bit.RWBit(0x07, 5)

	"""
	_inthl = i2c_bits.RWBits(8, 0x08, 0)
	_inthh = i2c_bits.RWBits(4, 0x09, 0)
	_intll = i2c_bits.RWBits(8, 0x0A, 0)
	_intlh = i2c_bits.RWBits(4, 0x0B, 0)
	_ihysl = i2c_bits.RWBits(8, 0x0C, 0)
	_ihysh = i2c_bits.RWBits(4, 0x0D, 0)
	"""

	#_tthl = Adafruit_bitfield({'TEMP':8})
	_tthl = i2c_bits.RWBits(8, 0x0E, 0)

	#_tthh = Adafruit_bitfield({'TEMP':3, 'SIGN':1})
	_tthh = i2c_bits.RWBits(4, 0x0F, 0)


	def __init__(self, i2c, addr=0x69):
		self.i2c_device = I2CDevice(i2c, addr)

		#enter normal mode
		self._pctl = 0x00

		#software reset
		self._rst = 0x3F

		#disable interrupts by default
		self.disableInterrupt()

		#set to 10 FPS
		self._fps = 0x00

	def disableInterrupt(self):
		self._inten = 0

	def readThermistor(self):
		raw = (self._tthh << 8) | self._tthl
		return self.signedMag12ToFloat(raw) * AMG88xx_THERMISTOR_CONVERSION

	def readPixels(self):
		retbuf = []
		buf = bytearray(3)

		with self.i2c_device as i2c:
			for i in range(0, AMG88xx_PIXEL_ARRAY_SIZE):
				buf[0] = AMG88xx_PIXEL_OFFSET + (i << 1)
				i2c.write(buf, end=1, stop=False)
				i2c.readinto(buf, start=1)
				
				raw = (buf[2] << 8) | buf[1]
				converted = self.signedMag12ToFloat(raw) * AMG88xx_PIXEL_TEMP_CONVERSION
				retbuf.append(converted)

		return retbuf

	def signedMag12ToFloat(self, val):
		#take first 11 bits as absolute val
		absVal = (val & 0x7FF)
		if val & 0x8000:
			return 0 - float(absVal)
		else:
			return float(absVal)
