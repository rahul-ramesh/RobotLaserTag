import httplib2
import math
import time
import numpy as np     

def sendCommand(connection, command):
    cmd = ""
    for v in command.split():
        cmd += chr(int(v))

    if(cmd == "fire"):
    	#TODO make sure proper syntax for POST request
    	h.request(fire_ip)
    
    else:
    	connection.write(cmd)


def main:
	
	#create map 2d array
	dir = 0
	map = []
	for i in range(0, 300):
		row = []
		for j in range(0, 300):
			row.append(0)
		map.append(row)

	#setup server connection
	h = httplib2.Http(".cache")
	loc_ip = "http://:80"
	cmd_ip = "http://:80"
	fire_ip = "http://:80"

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

		time.sleep(.1)


main