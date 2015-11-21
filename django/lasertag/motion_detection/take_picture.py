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
		location = analyze()
		print location
		#send to server
		if location == []:
			continue
		urllib.urlopen("http://192.168.43.130:80/robot_tag/" + str(location[0]).zfill(3) + str(location[1]).zfill(3) + "/add/")
		time.sleep(1)

def analyze_blue():
	os.system("streamer -c /dev/video1 -o map.jpeg")
	img_rgb = cv2.imread('map.jpeg')
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread('roomba_core.jpeg',0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)
	arr = zip(*loc[::-1])
	for pt in arr:
	    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

	cv2.imwrite('res.jpg',img_rgb)
	if arr != []:
		return arr[0]

	return arr


def analyze_red():
	os.system("streamer -c /dev/video1 -o map.jpeg")
	img_rgb = cv2.imread('map.jpeg')
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread('roomba_core.jpeg',0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)
	arr = zip(*loc[::-1])
	for pt in arr:
	    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

	cv2.imwrite('res.jpg',img_rgb)
	if arr != []:
		return arr[0]

	return arr

main()
