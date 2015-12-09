import httplib2
import serial
import time
import nanotime
import numpy as np
import math
import struct


def update_angle():
	global ang, last_command, time_spent, h, ang_ip
	if(time_spent == 0 or last_command == None or last_command == '145s0s0s0s0'):
		return
	radius = 235
	cmd = last_command.split('s')
	right = (int(cmd[1]) << 8) + int(cmd[2])  
	left  = (int(cmd[3]) << 8) + int(cmd[4])
	if(left > (1 << 15)):
		left = left - (1 << 16)

	if(right > (1 << 15)):
		right = right - (1 << 16) 
	left_dist = left * time_spent.seconds()
	right_dist = right * time_spent.seconds()
	print left, right, time_spent.seconds()
	ang = (ang + int(math.degrees((left_dist - right_dist)/ radius))) % 360
	print "Updating angle to: " + str(ang)
	resp, content = h.request(ang_ip + str(ang).zfill(3) + '/')

def injectFault(cmds, fault):
    global last_command
    right_vel = (int(cmds[1]) << 8) + int(cmds[2])  
    left_vel  = (int(cmds[3]) << 8) + int(cmds[4]) 

    cmd = chr(145)
    if(fault[0] == 'left'):
        vel = (int(cmds[3]) << 8) + int(cmds[4])
        if(vel > (1 << 15)):
            negVel = vel - (1 << 16)
            left_vel = int(negVel  * (100 - int(fault[1]))/100.0) + (1 << 16)
        else:
            left_vel = int(vel  * (100 - int(fault[1]))/100.0)

    else:
        vel = (int(cmds[1]) << 8) + int(cmds[2])
        if(vel > (1 << 15)):
            negVel = vel - (1 << 16)
            right_vel = int(negVel  * (100 - int(fault[1]))/100.0) + (1 << 16)
        else:
            right_vel = int(vel  * (100 - int(fault[1]))/100.0)
    
    update_angle()

    right_hi = right_vel >> 8
    right_lo = right_vel % 256 
    left_hi  = left_vel >> 8
    left_lo  = left_vel % 256
    last_command = '145s' + str(right_hi) + 's' + str(right_lo) + 's' + str(left_hi) + 's' + str(left_lo)
    

    cmd += chr(right_hi)
    cmd += chr(right_lo)
    cmd += chr(left_hi)
    cmd += chr(left_lo)
    return cmd

def sendCommand(connection, command):
	global h, fault

	ip_addr = "http://54.218.43.192/robot_tag/"
	team = "1"
	fire_ip = ip_addr + team + "/fire/"
	cmd = ""

	cmds = command.split('s')
	if(cmds[0] == '145'):
		if(fault == None):
			print "Sending: " + command + " Fault Free"
			for v in cmds:
	            		cmd += chr(int(v))
    		else:
    			if(command != '145s0s0s0s0'):
    				print "Sending: " + command + " With Fault: " + str(fault)
    			cmd = injectFault(cmds, fault)

    	elif(cmds[0] == '128' or cmds[0] == '142' or cmds[0] == '141'):
        	for v in cmds:
        		cmd += chr(int(v))

    	elif(cmds[0] == 'fire'):
    		print "Fire!"
        	h.request(fire_ip)
        	return 

    	else:
    		print 'Docking: ' + str(cmds)
    		connection.write(chr(143))
    		#docked = False
    		#while(not docked):
    		#	connection.write(chr(142) + chr(21))
    		#	docked = (get8Unsigned(connection) != 0)
       		return
	
	if(command != '145s0s0s0s0' and command != '142s20'):
		print "Writing: " + str(cmd.split('\\'))
	try:
    		if connection is not None:
        		connection.write(cmd)
        	else:
        		print "Not connected."
        except serial.SerialException:
        	print "Lost connection"
        	connection = None



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


def calculateExpectedLoc(angle, loc, cmds):
	expected_loc = loc
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
	return expected_loc

def adjustCommand(command, fault):
	if(fault != None):
		broken_wheel = fault[0]
		percent_lost = fault[1]
	else:
		broken_wheel = 'none'
		percent_lost = 0
	faulty_cmd = command.split('s')
	if(len(faulty_cmd) < 5):
		return command
	right_vel = (int(faulty_cmd[1]) << 8) + int(faulty_cmd[2])  
	left_vel  = (int(faulty_cmd[3]) << 8) + int(faulty_cmd[4]) 
	right_hi = faulty_cmd[1]
	right_lo = faulty_cmd[2] 
	left_hi  = faulty_cmd[3]
	left_lo  = faulty_cmd[4] 
	if(broken_wheel == 'right'):
		if(left_vel > (1 << 15)):
			left_vel = left_vel - (1 << 16)
			fixed_left_vel = int((100 - percent_lost)/100.0 * left_vel) + (1 << 16)
		else:
			fixed_left_vel = int((100 - percent_lost)/100.0 * left_vel)
		left_hi = fixed_left_vel >> 8
		left_lo = fixed_left_vel % 256
	elif(broken_wheel == 'left'):
		if(right_vel > (1 << 15)):
			right_vel = right_vel - (1 << 16)
			fixed_right_vel = int((100 - percent_lost)/100.0 * right_vel) + (1 << 16)
		else:
			fixed_right_vel = int((100 - percent_lost)/100.0 * right_vel)
		right_hi = fixed_right_vel >> 8
		right_lo = fixed_right_vel % 256
	else:
		return command 
	cmd = '145s' + str(right_hi) + 's' + str(right_lo) + 's' + str(left_hi) + 's' + str(left_lo)
	return cmd

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

def isolateFault(cmds, fault):
	global connection
	if(cmds == '145s0s0s0s0'):
		return fault

	sendCommand(connection, '142s41')
	right = get16Signed(connection)
	sendCommand(connection, '142s42')
	left = get16Signed(connection)
	cmd = cmds.split('s')
	if(len(cmd) < 5):
		return fault
	right_cmd = (int(cmd[1]) << 8) + int(cmd[2])
	left_cmd  = (int(cmd[3]) << 8) + int(cmd[4]) 
	if(left != left_cmd):
		power_lost = 100 - int((left * 1.0)/left_cmd * 100)
		return 'left', power_lost
	elif(right != right_cmd):
		power_lost = 100 - int((right * 1.0)/right_cmd * 100)
		return 'right', power_lost
	else:
		return None

def main():
	global connection, h, fault, ang, time_spent, ang_ip, last_command
	#init server connection
	h = httplib2.Http(".cache")

	ip_addr = "http://54.218.43.192/robot_tag/"
	team = "1"

	loc_ip = ip_addr + team +"/coords/"
	add_coords_ip = ip_addr + team + "/add_coords/"
	cmd_ip = ip_addr + team + "/command/"
	fire_ip = ip_addr + team + "/fire/"
	ang_ip = ip_addr + team + "/add_angles/"
	fault_ip = ip_addr + team + "/faults/"

	#init serial connection
	#port = "/dev/ttyUSB0"
	port = "/dev/tty.usbserial-DA01NZS8"
	connection = serial.Serial(port, baudrate=19200, timeout = 1)
	sendCommand(connection, '128s131')

	#grab inital loc from server
	resp, content = h.request(loc_ip)
	coords = content.split()
	loc = [coords[1], coords[2]]


	#init variables
	cmd_served = 0
	fault_served = 0
	fault = None
	detected_fault = None
	ang = 0
	last_time = nanotime.now()
	expected_loc = loc
	time_spent = 0
	start = 0
	last_command = None


	while True:
		#grab location from server
		resp, content = h.request(loc_ip)
		coords = content.split()
		if(len(coords) > 2):
			loc = [int(coords[1]), int(coords[2])]
			#print "Received loc: " + str(loc)

		#get fault from server
		resp, content = h.request(fault_ip)
		faults = content.split()
		if(len(faults) > 3 and int(faults[3]) > fault_served):
			fault_served = int(faults[3])
			if(faults[1] == '1'):
				wheel = 'left'
			elif(faults[1] == '2'):
				wheel = 'right'
			else:
				wheel = 'none' 
			print "Received Fault: " + wheel + ' ' + faults[2]
			fault = [wheel, int(faults[2])]

		#grab command from server
		resp, content = h.request(cmd_ip)
		cmds = content.split()
		if(int(cmds[2]) > cmd_served):
			print "Received cmd: " + cmds[1]
			cmd_served = int(cmds[2])
			last_time = nanotime.now()

			#adjust command for fault
			cmd = adjustCommand(cmds[1], detected_fault)
			if(fault != None):
				print "Adjusted command to: " + cmd
			else:
				print "No fault, command: " + cmd

			#send command to robot

			end = nanotime.now()
			sendCommand(connection, cmd)
			if(start != 0):
				time_spent = end - start
			start = nanotime.now()



			#calculate expected location
			#expected_loc = calculateExpectedLoc(ang, loc, cmd)

		#if no command then stop
		else:
			sendCommand(connection, '145s0s0s0s0')

		#check for fault
		#detected_fault = isolateFault(cmd, detected_fault)
		detected_fault = fault
		

		#check for timeout
        	if((nanotime.now() - last_time).minutes() > 4):
        		last_time = nanotime.now()
	        	sendCommand(connection, '143')

		time.sleep(.05)

main()
