import httplib2
import math
import time
import numpy as np 
import nanotime
import serial
import RPi.GPIO as GPIO    

def sendCommand(connection, command):
    cmd = ""
    write = False

    cmds = command.split('s')
    if(cmds[0] != '145' and cmds[0] != 'fire' and cmds[0] != '128'):
    	connection.write(chr(int('143')))
    	return

    for v in cmds:
        if(v == "fire"):
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
        
def main():
	
	#create map 2d array
	dir = 0
	ang = 0
	loc = [0,0]
	map = []
	for i in range(0, 300):
		row = []
		for j in range(0, 300):
			row.append(0)
		map.append(row)


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
	port = "/dev/ttyUSB0"
	connection = serial.Serial(port, baudrate=115200, timeout = 1)
	sendCommand(connection, '128s131')


	#Decided how to move the robot
	last_command = None
	served = 0
	while True:
		
		#get position from the server and parse position
		resp, content = h.request(loc_ip)
		coords = content.split()
		loc = [int(coords[1]), int(coords[2])]

		#get commands from server
		resp, content = h.request(cmd_ip)
		cmds = content.split()
		if(cmds[2] > served):
			served = cmds[2]
			sendCommand(connection, cmds[1])


			#calculate expected position
			#begin with calculating time
			if(last_command != None):
				loops = 0
				cmd = last_command.split('s')
				if(cmd == 'fire'):
					break
				right_vel = int(cmd[1]) << 8 + int(cmd[2])  
				left_vel  = int(cmd[3]) << 8 + int(cmd[4]) 
				if(right_vel == 0 or left_vel == 0):
					expected_loc[0] = loc[0]
					expected_loc[1] = loc[1]
				expected_loc[0] = (1) 
				expected_loc[1] = (1)

			last_command = cmds[1]
		else:
			sendCommand(connection, '145s0s0s0s0')

        #get angle and send it to the server
		#connection.write(connection, '20')
        #angChange = get16signed(connection)
        #ang = ang + angChange
        #resp, content = h.request(ang_ip + ang + '/')
		time.sleep(.1)


main()
