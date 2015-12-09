import sys
import httplib2
import termios
import tty

# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch(): 
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


def main():

	#connect to server
	h = httplib2.Http(".cache")
	cmd_ip = "http://54.218.43.192/robot_tag/1/add_command/"
	

	while True:
		#get input
		charIn = getch()


		#parse input into command

		#if up 
		if(charIn == 'w'):
			cmd = '145s0s250s0s250'

		#if down
		elif(charIn == 's'):
			cmd = '145s255s6s255s6'
			
		#if left
		elif(charIn == 'a'):
			cmd = '145s0s100s255s156'
			
		#if right
		elif(charIn == 'd'):
			cmd = '145s255s156s0s100'
			
		#if fire
		elif(charIn == 'l'):
			cmd = 'fire'

		elif(charIn == 'q'):
			cmd = '128s131'

		#exit
		elif(charIn == 'p'):
			exit()

		else:
			cmd = '198765'

		sent = cmd_ip + cmd + '/'
		print sent
		resp, contents = h.request(sent)
		print resp
	print "escaped"

main()

