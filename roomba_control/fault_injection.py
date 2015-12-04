import httplib2
import math
import time
import numpy as np 
import nanotime
import serial
import struct

def main():
    var = 'n'
    while (var != 'd'):
        cmd = ""
        cmds = raw_input("Please enter cmd: ").split()
        fault = raw_input("Please enter fault: ").split()

        if(fault[0] == 'left'):
            cmd += chr(int(cmds[1]))
            cmd += chr(int(cmds[2]))
            vel = (int(cmds[3]) << 8) + int(cmds[4])
            if(vel > 32768):
                faultyVel = (0xFE00) | int(vel  * (100 - int(fault[1]))/100.0)
            else:
                faultyVel = int(vel  * int((100 - int(fault[1]))/100.0))
            print faultyVel, faultyVel >> 8, faultyVel % 256
            cmd += chr(faultyVel >> 8)
            cmd += chr(faultyVel % 256)

        else:
            vel = (int(cmds[1]) << 8) + int(cmds[2])
            if(vel > 32768):
                faultyVel = (0xFE00) | int(vel  * (100 - int(fault[1]))/100.0)
            else:
                faultyVel = int(vel  * int((100 - int(fault[1]))/100.0))
            cmd += chr(faultyVel >> 8)
            cmd += chr(faultyVel % 256)
            cmd += chr(int(cmds[3]))
            cmd += chr(int(cmds[4]))

        print cmds
        print fault
        print cmd

main()