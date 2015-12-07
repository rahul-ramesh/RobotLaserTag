import httplib2
import serial
import time
import nanotime
import numpy as np
import math
import struct

def injectFault(cmds, fault):
    cmd = ""
    if(fault[0] == 'left'):
        cmd += chr(int(cmds[1]))
        cmd += chr(int(cmds[2]))
        vel = (int(cmds[3]) << 8) + int(cmds[4])
        if(vel > (1 << 15)):
            negVel = vel - (1 << 16)
            faultyVel = int(negVel  * (100 - int(fault[1]))/100.0) + (1 << 16)
        else:
            faultyVel = int(vel  * (100 - int(fault[1]))/100.0)
        cmd += chr(faultyVel >> 8)
        cmd += chr(faultyVel % 256)

    else:
        vel = (int(cmds[1]) << 8) + int(cmds[2])
        if(vel > (1 << 15)):
            negVel = vel - (1 << 16)
            faultyVel = int(negVel  * (100 - int(fault[1]))/100.0) + (1 << 16)
        else:
            faultyVel = int(vel  * (100 - int(fault[1]))/100.0)
        cmd += chr(faultyVel >> 8)
        cmd += chr(faultyVel % 256)
        cmd += chr(int(cmds[3]))
        cmd += chr(int(cmds[4]))
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
			for v in cmds:
                            cmd += chr(int(v))
    		else:
    			cmd = injectFault(cmds, fault)

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
    			docked = (get8Unsigned(connection) != 0)
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


def calculateExpectedLoc(angle, loc, cmds):
	expected_loc = [0,0]
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
	if(cmds == '145s0s0s0s0'):
		return fault

	sendCommand(connection, '142s41')
	right = get16Signed(connection)
	sendCommand(connection, '142s42')
	left = get16Signed(connection)
	cmd = cmds.split('s')
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
	port = "/dev/ttyUSB0"
	connection = serial.Serial(port, baudrate=115200, timeout = 1)
	sendCommand(connection, '128s131')

	#grab inital loc from server
	resp, content = h.request(loc_ip)
	coords = content.split()
	loc = [coords[1], coords[2]]

	#init angle reading
	sendCommand(connection, '142s20')
	get16Signed(connection)

	#init variables
	cmd_served = 0
	fault_served = 0
	fault = None
	ang = 0
	last_time = nanotime.now()
	expected_loc = loc


	while True:
		#grab location from server
		resp, content = h.request(loc_ip)
		coords = content.split()
		loc = [int(coords[1]), int(coords[2])]

		#get fault from server
		resp, content = h.request(fault_ip)
		faults = content.split()
		if(len(faults) > 2 and int(faults[3]) > fault_served):
			fault_served = int(faults[3])
			fault = [faults[1], int(faults[2])]

		#grab command from server
		resp, content = h.request(cmd_ip)
		cmds = content.split()
		if(int(cmds[2]) > cmd_served):
			cmd_served = int(cmds[2])
			last_time = nanotime.now()

			#adjust command for fault
			cmd = adjustCommand(cmds[1], fault)

			#send command to robot
			sendCommand(connection, cmd)

			#calculate expected location
			#expected_loc = calculateExpectedLoc(ang, loc, cmd)

		#if no command then stop
		else:
			sendCommand(connection, '145s0s0s0s0')

		#check for fault
		fault = isolateFault(cmd)

		#update angle
		sendCommand(connection, '142s20')
		ang_change = get16Signed(connection)
		angle = (ang + ang_change) % 360

		#check for timeout
        if((nanotime.now() - last_time).minutes() > 5):
        	last_time = nanotime.now()
	        sendCommand(connection, '143')

		time.sleep(.05)

main()
