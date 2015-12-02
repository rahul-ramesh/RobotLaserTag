import httplib2
import math
import time
import numpy as np 
import nanotime
import serial
#import RPi.GPIO as GPIO    

def sendCommand(connection, command):
	global h, fault

	ip_addr = "http://http://54.218.43.192/robot_tag/"
	team = "1"
	fire_ip = ip_addr + team + "/fire/"
	cmd = ""

	cmds = command.split('s')
	if(cmds[0] == '145'):
		if(fault == None):
			for v in cmds:
    				cmd += chr(int(v))
    		else:
    			cmd += chr(int(cmds[0]))
    			if(fault[0] == 'left'):
    				cmd += chr(int(cmds[1]))
    				cmd += chr(int(cmds[2]))
    				vel = int(int(cmds[3]) << 8 + int(cmds[4]) * fault[1])
    				cmd += chr(vel >> 8)
    				cmd += chr(vel % 256)

    			else:
    				vel = int(int(cmds[1]) << 8 + int(cmds[2]) * fault[1])
    				cmd += chr(vel >> 8)
    				cmd += chr(vel % 256)
    				cmd += chr(int(cmds[3]))
    				cmd += chr(int(cmds[4]))

    	elif(cmds[0] == '128' or cmds[0] == '142' or cmds[0] == '141'):
        	for v in cmds:
        		cmd += chr(int(v))

    	elif(cmds[0] == 'fire'):
        	h.request(fire_ip)
        	return 

    	else:
    		connection.write(chr(143))
    		docked = False
    		while(not docked):
    			connection.write(chr(142) + chr(21))
    			docked = get8Unsigned(connection) > 0
       		return

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
      
def distanceBetween(loc, expected_loc):
	return math.hypot(expected_loc[0] - loc[0], expected_loc[1] - loc[1])

def findFault(loc, expected_loc, prev_loc, command):
	if(command == None):
		return None, 0
	vec_loc = np.array(loc)
	vec_expected_loc = np.array(expected_loc)
	vec_prev_loc = np.array(prev_loc)
	vec_expected = vec_expected_loc - vec_prev_loc
	vec_real = vec_loc - vec_prev_loc
	angle = math.degrees(math.acos(np.dot(vec_real, vec_expected)/(np.linalg.norm(vec_real) * np.linalg.norm(vec_expected))))
	broken_wheel = 'right' if (0 < angle < 90 or 180 < angle < 270) else 'left'
	percent_lost = (angle % 90) * (10.0/9.0)
	return broken_wheel, percent_lost

def adjustCommand(command, broken_wheel, percent_lost):
	faulty_cmd = command.split('s')
	right_vel = int(faulty_cmd[1]) << 8 + int(faulty_cmd[2])  
	left_vel  = int(faulty_cmd[3]) << 8 + int(faulty_cmd[4]) 
	right_hi = faulty_cmd[1]
	right_lo = faulty_cmd[2] 
	left_hi  = faulty_cmd[3]
	left_lo  = faulty_cmd[4] 
	if(broken_wheel == 'right'):
		fixed_left_vel = int(percent_lost * left_vel)
		left_hi = fixed_left_vel >> 8
		left_lo = fixed_left_vel % 256
	elif(broken_wheel == 'left'):
		fixed_right_vel = int(percent_lost * right_vel)
		right_hi = fixed_right_vel >> 8
		right_lo = fixed_right_vel % 256
	else:
		return command 
	cmd = '145s' + right_hi + 's' + right_lo + 's' + left_hi + 's' + left_lo 
	return cmd

def main():
	global h, fault

	#setup server connection
	h = httplib2.Http(".cache")
	
	ip_addr = "http://http://54.218.43.192/robot_tag/"
	team = "1"

	loc_ip = ip_addr + team +"/coords/"
	add_coords_ip = ip_addr + team + "/add_coords/"
	cmd_ip = ip_addr + team + "/command/"
	fire_ip = ip_addr + team + "/fire/"
	ang_ip = ip_addr + team + "/add_angles/"
	fault_ip = ip_addr + team + "/faults/"

	#connet to roomba
	port = "/dev/ttyUSB0"
	connection = serial.Serial(port, baudrate=115200, timeout = 1)
	sendCommand(connection, '128s131')


	#initialize logic variables	
	last_command = None
	bad_wheel = None
	fault = None
	percent_lost = 0
	served_cmd = 0
	served_fault = 0
	expected_loc = [0,0]
	last_time = nanotime.now()
	angle = 0
	loc = [0,0]
	#TODO: How many cm's to a map unit
	scale = .7

	#Decided how to move the robot
	while True:
		
		#get position from the server and parse position
		resp, content = h.request(loc_ip)
		coords = content.split()
		prev_loc = loc
		loc = [int(coords[1]), int(coords[2])]

		#check for any discepency in expected position
		if(distanceBetween(loc, expected_loc) > 5):
			print "Found fault! Expected: " 
			print expected_loc 
			print "But got: "
			print loc
			sendCommand(connection, '141 1')
			bad_wheel, percent_lost = findFault(loc, expected_loc, prev_loc, last_command)			

		#get fault from server
		resp, contents = h.request(fault_ip);
		faults = contents.split()
		if(faults[3] > served_fault):
			served_fault = faults[3]
			fault = [faults[1], int(faults[2])]


		#get commands from server
		resp, content = h.request(cmd_ip)
		if(contents == "No commands present!"):
			continue
		cmds = content.split()
		if(cmds[2] > served_cmd):
			last_time = nanotime.now()
			served_cmd = cmds[2]
			sendCommand(connection, '128s131')
			sendCommand(connection, adjustCommand(cmds[1], broken_wheel, percent_lost))
			last_command = cmds[1]

			#calculate expected position
			#begin with calculating time
			cmd = cmds[1].split('s')
			if(len(cmd) < 5):
				continue
			right_vel = int(cmd[1]) << 8 + int(cmd[2])  
			left_vel  = int(cmd[3]) << 8 + int(cmd[4]) 
			if(right_vel == left_vel):
				forward = 1 if(reight_vel == 500) else -1
				expected_loc[0] = int(round(loc[0] + forward * math.cos(math.radians(angle)) * 5 * scale))
				expected_loc[1] = int(round(loc[1] + forward * math.sin(math.radians(angle)) * 5 * scale))
			else:
				expected_loc[0] = loc[0]
				expected_loc[1] = loc[1]

		else:
			sendCommand(connection, '145s0s0s0s0')

		#update angle
		sendCommand(connection, '142 20')
		ang_change = get16Signed(connection)
		angle = (angle + ang_change) % 360
		h.request(ang_ip + "{0:0=3d}".format(angle) + '/')

        
        	#check for timeout
        	time_taken = (nanotime.now() - last_time).minutes()
        	if(time_taken > 5):
        		last_time = nanotime.now()
			sendCommand(connection, '143')
		time.sleep(.1)


main()
