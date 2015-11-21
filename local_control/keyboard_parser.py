import sys
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
        if(ch == ' '):
            exit()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def main():

	#connect to server
	h = httplib2.Http(".cache")
    cmd_ip = "http://:8000/robot_tag/1/"
	

    while True:
		#get input
        charIn = getch()
		#parse input into command
        cmd = '145 '
		#if up 
        if(charIn == 'w'):
            cmd =  cmd + '1 244 1 244'

		#if down
        elif(charIn == 's'):
			cmd = cmd + "254 12 254 12"
			
		#if left
        elif(charIn == 'a'):
			cmd = cmd + '1 244 254 12'
			
		#if right
        elif(charIn == 'd'):
			cmd = cmd + '254 12 1 244'
			
        elif(charIn == "k"):
            cmd = 'Fire'

        else:
            cmd = charIn

        print "cmd: " + cmd
		h.request(cmd_ip + cmd + "/add_command/")

main()

