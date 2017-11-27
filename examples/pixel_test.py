import busio
import adafruit_amg88xx
import board
import time

myI2C = busio.I2C(board.SCL, board.SDA)

amg = adafruit_amg88xx.Adafruit_AMG88xx(myI2C)

def chunks(l, n):
	#break list into n sized chunks
	for i in range(0, len(l), n):
		yield l[i:i + n]

while True:
	value = amg.readPixels()
	
	#format the output as nice rows of 8 pixels
	chunked = list(chunks(value, 8))
	for c in chunked:
		#pad to 1 decimal place
		print(['{0:.1f}'.format(x) for x in c])
		print("")
		
	print("\n")
	time.sleep(1)