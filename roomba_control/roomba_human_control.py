import httplib2
import math
import time
import numpy as np 
import RPi.GPIO as GPIO    

def sendCommand(connection, command):
    cmd = ""
    for v in command.split():
        cmd += chr(int(v))

    if(cmd == "fire"):
    	#TODO make sure proper syntax for POST request
    	h.request(fire_ip)
    	GPIO.output(18, true)
    	time.sleep(.5)
    	GPIO.output(18, false)
    
    else:
    	connection.write(cmd)

# getDecodedBytes returns a n-byte value decoded using a format string.
# Whether it blocks is based on how the connection was set up.
def getDecodedBytes(connection, n, fmt):
    
    try:
        return struct.unpack(fmt, connection.read(n))[0]
    except serial.SerialException:
        print "Lost connection"
        connection = None
        return None
    except struct.error:
        print "Got unexpected data from serial port."
        return None

# get8Unsigned returns an 8-bit unsigned value.
def get8Unsigned(connection):
    return getDecodedBytes(connection, 1, "B")

# get8Signed returns an 8-bit signed value.
def get8Signed(connection):
    return getDecodedBytes(connection, 1, "b")

# get16Unsigned returns a 16-bit unsigned value.
def get16Unsigned(connection):
    return getDecodedBytes(connection, 2, ">H")

# get16Signed returns a 16-bit signed value.
def get16Signed(connection):
    return getDecodedBytes(connection, 2, ">h")
        
def main:
	
	#create map 2d array
	dir = 0
    ang = 0;
	map = []
	for i in range(0, 300):
		row = []
		for j in range(0, 300):
			row.append(0)
		map.append(row)

	#setup GPIO pin
	GPIO.setup(18, GPIO.out)

	#setup server connection
	h = httplib2.Http(".cache")
	loc_ip = "http://:80"
	cmd_ip = "http://:80"
	fire_ip = "http://:80"
    ang_ip = "http://:80"

	#connet to roomba
	port = "/dev/ttyUSB0"
	connection = serial.Serial(port, baudrate=115200, timeout = 1)
	sendCommand('128 131', connection)


	#Decided how to move the robot
	while True:
		
		#get position from the server and parse position
		resp, content = h.request(loc_ip)
		coords = content.split()
		loc = [int(coords[0]), int(coords[1])]

		#get commands from server
		resp, content h.request(cmd_ip)
		sendCommand(connection, content)

        #get angle and send it to the server
        connection.write(connection, '20')
        angChange = get16signed(connection)
        ang = ang + angChange
        resp, content = h.request(ang_ip)

		time.sleep(.1)
		sendCommand('145 0 0 0 0', connection)


main
