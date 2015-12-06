import httplib2
import math
import time
import numpy as np 
import nanotime
import serial
import struct

def main(cmds):
	global h, fault

	#setup server connection
	h = httplib2.Http(".cache")
	
	ip_addr = "http://54.218.43.192/robot_tag/"
	team = "1"

	loc_ip = ip_addr + team +"/coords/"
	add_coords_ip = ip_addr + team + "/add_coords/"
	cmd_ip = ip_addr + team + "/command/"
	fire_ip = ip_addr + team + "/fire/"
	ang_ip = ip_addr + team + "/add_angles/"
	fault_ip = ip_addr + team + "/faults/"

	#connet to roomba
	#port = "/dev/ttyUSB0"
	#connection = serial.Serial(port, baudrate=115200, timeout = 1)
	#sendCommand(connection, '128s131')


	#initialize logic variables	
	expected_loc = [0,0]
	angle = 45 + 180
	loc = [150,150]
	scale = 1


	#calculate expected position
	cmd = cmds.split('s')
	right_vel = (int(cmd[1]) << 8) + int(cmd[2]) 
	left_vel  = (int(cmd[3]) << 8) + int(cmd[4]) 
	if(right_vel == left_vel):
		forward = 1 if(right_vel == 500) else -1
		expected_loc[0] = loc[0] + int(round(forward * math.cos(math.radians(angle)) * 5 * scale))
		expected_loc[1] = loc[1] + int(round(forward * math.sin(math.radians(angle)) * 5 * scale))
	else:
		expected_loc[0] = loc[0]
		expected_loc[1] = loc[1]

	print loc
	print cmd
	print expected_loc




while True:
	var = raw_input("Please enter cmd: ")
	main(var)
