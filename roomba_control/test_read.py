import httplib2
import math
import time
import numpy as np 
import nanotime
import serial
import struct

def sendCommand(connection, command):
    cmd = ""
    write = False

    cmds = command.split()

    for v in cmds:
        if(cmd == "fire"):
    		h.request(fire_ip)
        	
        else:
        	write = True
        	cmd += chr(int(v))
    	

    if(write):
    	connection.write(cmd)

# getDecodedBytes returns a n-byte value decoded using a format string.
# Whether it blocks is based on how the connection was set up.
def getDecodedBytes(connection, n, fmt):
    
    try:
    	print "Getting encoded bytes..."
    	read = connection.read(n)
    	print "Read: " + read
        return struct.unpack(fmt, read)[0]
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
        
def main():
	

	#setup server connection
	h = httplib2.Http(".cache")
	
	ip_addr = "http://0.0.0.0:8000/robot_tag/"
	team = "1"

	loc_ip = ip_addr + team +"/coords/"
	add_coords_ip = ip_addr + team + "/add_coords/"
	cmd_ip = ip_addr + team + "/command/"
	fire_ip = ip_addr + team + "/fire/"
	ang_ip = ip_addr + team + "/add_angles/"

	#connet to roomba
	port = "/dev/tty.usbserial-DA01NZOS"
	connection = serial.Serial(port, baudrate=115200, timeout = 1)
	sendCommand(connection, '128 131')


	#Decided how to move the robot
	while True:
		
		sendCommand(connection, '43')
		left = get16Unsigned(connection)
		time.sleep(1)


main()
