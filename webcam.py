#!/bin/python2

import sys, getopt
import cv2

class WebcamInterface(object):
	def __init__(self, device):
		cv2.namedWindow("wcapture")
		self.capture = cv2.VideoCapture(device)
		self.rval = None
		self.frame = None
		
	def capture_frame(self):
		if self.capture.isOpened():
			self.rval, self.frame = self.capture.read()
		
	def show(self):
		while self.frame <> None:
			cv2.imshow("wcapture", self.frame)
			if cv2.waitKey(10) == 27:
				break
		
	def save(self, filename):
		cv2.imwrite(filename, self.frame)

if __name__ == '__main__':
	wif = None
	device = 0
	output = None
	show = False
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hd:o:s:", ["help", "device=", "output=", "show"])
	except getopt.GetoptError:
		print 'Usage: webcam.py [OPTION] <VALUE>'
		sys.exit(2)
		
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			pass
		
		if opt in ("-d", "--device"):
			try:
				device = int(arg)
			except:
				print 'Usage: webcam.py [OPTION] <VALUE>'
				sys.exit(2)
				
		if opt in ("-o", "--output"):
			output = arg
			
		if opt in ("-s", "--show"):
			show = True
			
	wif = WebcamInterface(device)
	
	if output <> None or show:
		wif.capture_frame()
	else:
		print 'Usage: webcam.py [OPTION] <VALUE>'
		sys.exit(2)
		
	if output <> None:
		wif.save(output)
		
	if show:
		wif.show()
