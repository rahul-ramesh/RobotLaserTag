#!/usr/bin/env/ python

import cv2
import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os
import urllib
import time

def main():
	while (1):
		os.system("streamer -c /dev/video0 -o map.jpeg")
		location1 = analyze_1()
		print " "
		print "location 1: " + str(location1)
		print " "
		location2 = analyze_2()
		print "location 2: " + str(location2)
		print " "
		#send to server
		if location1 != []:
			pass
			#urllib.urlopen("http://54.218.43.192/robot_tag/1/add_coords/" + str(location1[0]).zfill(3) + str(location1[1]).zfill(3) + "/")
		if location2 != []:
			pass
			#urllib.urlopen("http://54.218.43.192/robot_tag/2/add_coords/" + str(location2[0]).zfill(3) + str(location2[1]).zfill(3) + "/")
		time.sleep(0.5)

def analyze_1():
	#os.system("streamer -c /dev/video1 -o map.jpeg")
	img_rgb = cv2.imread('map.jpeg')
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread('roomba_yellow.jpeg',0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)
	arr = zip(*loc[::-1])
	for pt in arr:
	    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

	cv2.imwrite('res1.jpg',img_rgb)
	if arr != []:
		return arr[0]

	return arr

def analyze_2():
	#os.system("streamer -c /dev/video1 -o map.jpeg")
	img_rgb = cv2.imread('map.jpeg')
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread('roomba_green.jpeg',0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.9
	loc = np.where( res >= threshold)
	arr = zip(*loc[::-1])
	for pt in arr:
	    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

	cv2.imwrite('res2.jpg',img_rgb)
	if arr != []:
		return arr[0]

	return arr

main()
