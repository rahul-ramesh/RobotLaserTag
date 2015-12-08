import nanotime
import math

def main():
	while True:
		loc = [100, 100]
		cmds = '145s1s244s1s244'
		angle = 0

		cmd = cmds.split('s')
		right_vel = (int(cmd[1]) << 8) + int(cmd[2]) 
		left_vel  = (int(cmd[3]) << 8) + int(cmd[4]) 
		if(right_vel == left_vel):
			forward = 1 if(right_vel == 500) else -1
			expected_loc[0] = loc[0] + int(round(forward * math.cos(math.radians(angle)) * 5))
			expected_loc[1] = loc[1] + int(round(forward * math.sin(math.radians(angle)) * 5))
		else:
			expected_loc[0] = loc[0]
			expected_loc[1] = loc[1]


		for i in range(101):
			other_loc = 


main()