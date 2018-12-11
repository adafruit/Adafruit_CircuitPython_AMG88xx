Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-amg88xx/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/amg88xx/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_AMG88xx.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_AMG88xx
    :alt: Build Status


Adafruit CircuitPython module for the AMG88xx GRID-Eye IR 8x8 thermal camera.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Of course, you must import the library to use it:

.. code-block:: python

    import busio
    import adafruit_amg88xx

The way to create an I2C object depends on the board you are using. For boards with labeled SCL and SDA pins, you can:

.. code-block:: python

    import board

You can also use pins defined by the onboard microcontroller through the microcontroller.pin module.

Now, to initialize the I2C bus:

.. code-block:: python

    i2c_bus = busio.I2C(board.SCL, board.SDA)

Once you have created the I2C interface object, you can use it to instantiate the AMG88xx object

.. code-block:: python

    amg = adafruit_amg88xx.AMG88XX(i2c_bus)

You can also optionally use the alternate i2c address (make sure to solder the jumper on the back of the board if you want to do this)

.. code-block:: python

    amg = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)

Pixels can be then be read by doing:

.. code-block:: python

    print(amg.pixels)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-travis-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block::shell

    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt

Once installed, make sure you are in the virtual environment:

.. code-block::shell

    source .env/bin/activate

Then run the build:

.. code-block::shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-lis3dh --library_location .
