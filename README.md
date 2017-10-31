# Adafruit_CircuitPython_AMG88xx

# Dependencies

This driver depends on the Register and Bus Device libraries. Please ensure they are also available on the CircuitPython filesystem. This is easily achieved by downloading a library and driver bundle.

# Usage Notes

Basics

Of course, you must import the library to use it:

```
import busio
import adafruit_amg88xx
```
The way to create an I2C object depends on the board you are using. For boards with labeled SCL and SDA pins, you can:

```
from board import *
```

You can also use pins defined by the onboard microcontroller through the microcontroller.pin module.

Now, to initialize the I2C bus:

```
myI2C = busio.I2C(SCL, SDA)
```

Once you have created the I2C interface object, you can use it to instantiate the AMG88xx object

```
amg = adafruit_amg88xx.Adafruit_AMG88xx(myI2C)
```

You can also optionally use the alternate i2c address (make sure to solder the jumper on the back of the board if you want to do this)

```
amg = adafruit_amg88xx.Adafruit_AMG88xx(myI2C, addr=0x68)
```

# Reading Pixels

Pixels can be then be read by doing: 

```
value = a.readPixels()
print(value)
```
