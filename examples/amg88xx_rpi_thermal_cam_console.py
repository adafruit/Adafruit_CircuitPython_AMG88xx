"""This example is for Raspberry Pi (Linux) only!
   It will not work on microcontrollers running CircuitPython!"""

import os
import sys
import math
import time
import atexit
import busio
import board

import numpy as np
from scipy.interpolate import griddata

from colour import Color
from os import system, name
import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)

# low range of the sensor (this will be blue on the screen)
MINTEMP = 26.0

# high range of the sensor (this will be red on the screen)
MAXTEMP = 32.0

# how many color values we can have
COLORDEPTH = 1024

#os.putenv("SDL_FBDEV", "/dev/fb1")
#pygame.init()

# initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
# pylint: enable=invalid-slice-index

# sensor is an 8x8 grid so lets do a square
height = 240
width = 240

# the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

# create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
console_colors = [17,18,19,20,21,57,93,129,165,201,200,199,198,197,196,202,208,214,220]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

# some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clear(): 
    _ = system('clear') 

def print_there(x, y, text, color):
	sys.stdout.write("\x1b7\x1b[48;5;%dm" % (color))
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
maxpixel = 0
minpixel = 0
color_range = 1
def exit_handler():
    print("maxpixel:" + str(maxpixel))
    print("minpixel:" + str(minpixel))

atexit.register(exit_handler)
# let the sensor initialize
time.sleep(0.1)

while True:

    # read the pixels
    pixels = []
    for row in sensor.pixels:
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

    # perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")

    # draw everything
    y=2
    for ix, row in enumerate(bicubic):
        x=2
        for jx, pixel in enumerate(row):
            color_index = 0
            if (color_range != 0):
                color_index = int(round((pixel-minpixel)/color_range))
            if color_index < 0:
                color_index = 0
            if color_index > len(console_colors)-1:
                color_index = len(console_colors)-1
            print_there(x, y*2-2, '  ', console_colors[color_index])
            if pixel > maxpixel:
                maxpixel = pixel
            if pixel < minpixel:
                minpixel = pixel
            x+=1
        y+=1
    heat_range = maxpixel - minpixel
    color_range = heat_range / len(console_colors)
