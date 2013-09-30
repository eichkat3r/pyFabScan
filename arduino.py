#!/bin/python2

import serial
import time
import sys, getopt

# Command-constants
TURN_LASER_OFF    = 200
TURN_LASER_ON     = 201
PERFORM_STEP      = 202
SET_DIRECTION_CW  = 203
SET_DIRECTION_CCW = 204
TURN_STEPPER_ON   = 205
TURN_STEPPER_OFF  = 206
TURN_LIGHT_ON     = 207
TURN_LIGHT_OFF    = 208
ROTATE_LASER      = 209 # Unused
FABSCAN_PING      = 210
FABSCAN_PONG      = 211
SELECT_STEPPER    = 212 # Unused

class ArduinoInterface(object):
	def __init__(self, port):
		# Connect to the given serial port
		self._serial = serial.Serial(port, 9600)
		
		# Check for a pong signal (the arduino sends FABSCAN_PONG if
		# it is set up).
		if ord(self._serial.read(1)) == FABSCAN_PONG:
			print 'FabScan Shield is set up and ready.'
			
	def send(self, command):
		self._serial.write(chr(command))
		
	# Return true if the arduino is responding
	def ping(self):
		self.send(FABSCAN_PING)
		return ord(self._serial.read(1)) == FABSCAN_PONG
		
	def close(self):
		self._serial.close()

if __name__ == '__main__':
	aif = None
	device = None
	laser = None
	stepper = None
	turn = None
	ping = False
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hd:l:s:t:p", ["help", "device=", "laser=", "stepper=", "turn=", "ping"])
	except getopt.GetoptError:
		print 'Usage: arduino.py [OPTION] <VALUE>'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Usage: arduino.py [OPTION] <VALUE>'
			print 'Option:\t\tDescription:'
			print '-d --device\tSet device to VALUE'
			print '-l --laser\tTurn laser on (VALUE=1) or off (VALUE=0)'
			print '-s --stepper\tTurn stepper on (VALUE=1) or off (VALUE=0)'
			print '-t --turn\tTurn stepper around VALUE steps'
			print '-p --ping\tSend ping signal to Arduino'
			sys.exit()
		
		if opt in ("-d", "--device"):
			device = arg
		
		if opt in ("-l", "--laser"):
			if arg in ("0", "1"):
				laser = int(arg)
			else:
				print 'Usage: arduino.py [OPTION] <VALUE>'
				sys.exit(2)
		
		if opt in ("-s", "--stepper"):
			if arg in ("0", "1"):
				stepper = int(arg)
			else:
				print 'Usage: arduino.py [OPTION] <VALUE>'
				sys.exit(2)
				
		if opt in ("-t", "--turn"):
			try:
				turn = int(arg)
			except:
				print 'Usage: arduino.py [OPTION] <VALUE>'
				sys.exit(2)
				
		if opt in ("-p", "--ping"):
			ping = True
			
	if device <> None:
		aif = ArduinoInterface(device)
	else:
		aif = ArduinoInterface('/dev/ttyACM0')
		
	if laser <> None:
		if laser is 0:
			aif.send(TURN_LASER_OFF)
		if laser is 1:
			aif.send(TURN_LASER_ON)
			
	if stepper <> None:
		if stepper is 0:
			aif.send(TURN_STEPPER_OFF)
		if stepper is 1:
			aif.send(TURN_STEPPER_ON)

	if turn <> None:
		aif.send(PERFORM_STEP)
		aif.send(turn)
		
	if ping is True:
		if aif.ping():
			print 'Device has responded to ping.'
		else:
			print 'Device did not respond to ping.'
