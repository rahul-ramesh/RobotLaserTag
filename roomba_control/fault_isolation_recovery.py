import httplib2
import math
import time
import numpy as np 
import nanotime
import serial
import struct

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

def main(cmds, fault):
    cmd = ""
    if(fault[0] == 'left'):
        #cmd += chr(int(cmds[1]))
        #cmd += chr(int(cmds[2]))
        vel = (int(cmds[3]) << 8) + int(cmds[4])
        if(vel > (1 << 15)):
            negVel = vel - (1 << 16)
            faultyVel = int(negVel  * (100 - int(fault[1]))/100.0) + (1 << 16)
        else:
            faultyVel = int(vel  * (100 - int(fault[1]))/100.0)
        #cmd += chr(faultyVel >> 8)
        #cmd += chr(faultyVel % 256)
        cmd = cmds[0] + 's' + cmds[1] + 's' + cmds[2] + 's' + str(faultyVel >> 8) + 's' + str(faultyVel % 256) 


    else:
        vel = (int(cmds[1]) << 8) + int(cmds[2])
        if(vel > (1 << 15)):
            negVel = vel - (1 << 16)
            faultyVel = int(negVel  * (100 - int(fault[1]))/100.0) + (1 << 16)
        else:
            faultyVel = int(vel  * (100 - int(fault[1]))/100.0)
        #cmd += chr(faultyVel >> 8)
        #cmd += chr(faultyVel % 256)
        #cmd += chr(int(cmds[3]))
        #cmd += chr(int(cmds[4]))
        cmd = cmds[0] + 's' + str(faultyVel >> 8) + 's' + str(faultyVel % 256) + 's' + cmds[3] + 's' + cmds[4]
    return cmd

def test():
	commands = [['145', '1', '244', '1', '244'], ['145', '254', '12', '254', '12']]
	others = [['145', '254', '12', '1', '244'], ['145', '1', '244', '254', '12']]
	faults = ['left', 'right']

	for i in range(101):
		for j in range(2):
			for k in range(2):
				cmd = commands[j]
				fault = [faults[k], str(i)]
				final = adjustCommand(main(cmd, fault), fault[0], int(fault[1]))
				cmds = final.split('s')
				if(cmds[1] != cmds[3] or cmds[2] != cmds[4]):
					print cmd, fault, cmds

	print "Done with up/down. Moving to left/right."

	for i in range(101):
		for j in range(2):
			for k in range(2):
				cmd = others[j]
				fault = [faults[k], str(i)]
				final = adjustCommand(main(cmd, fault), fault[0], int(fault[1]))
				cmds = final.split('s')
				if(j == 0):
					val1 = (int(cmds[1]) << 8) + int(cmds[2]) - (1 << 16)
					val2 = (int(cmds[3]) << 8) + int(cmds[4])
				else:
					val1 = (int(cmds[1]) << 8) + int(cmds[2])
					val2 = (int(cmds[3]) << 8) + int(cmds[4]) - (1 << 16)
				if(val1 + val2 != 0):
					print cmd, fault, cmds
test()
