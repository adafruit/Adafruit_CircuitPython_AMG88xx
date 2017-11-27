import busio
import adafruit_amg88xx
import board
import time

myI2C = busio.I2C(board.SCL, board.SDA)

amg = adafruit_amg88xx.Adafruit_AMG88xx(myI2C)

while True:
	value = amg.readPixels()
	print(value)
	time.sleep(1)