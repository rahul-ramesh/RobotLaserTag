import serial


# sendCommandRaw takes a string interpreted as a byte array
def sendCommandRaw(connection, command):
    try:
        if connection is not None:
            connection.write(command)
        else:
            tkMessageBox.showerror('Not connected!', 'Not connected to a robot!')
            print "Not connected."
    except serial.SerialException:
        print "Lost connection"
        tkMessageBox.showinfo('Uh-oh', "Lost connection to the robot!")
        connection = None

# sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
def sendCommandASCII(connection, command):
    cmd = ""
    for v in command.split('s'):
        cmd += chr(int(v))

    sendCommandRaw(connection, cmd)


port = "/dev/tty.usbserial-DA01NZOS"
connection = serial.Serial(port, baudrate=19200, timeout = 1)
sendCommandASCII(connection, '128s131')
while(True):
	sendCommandASCII(connection, '139s15s255s255')