#Import OpenCV
import cv2
#Import Numpy
import numpy as np
import urllib

def main():
    camera_feed = cv2.VideoCapture(0)
    while(1):
	track_orange(camera_feed)
	track_green(camera_feed)
    	#If escape is pressed close all windows
    	if k == 27:
    	    break
    cv2.destroyAllWindows()

def track_orange(camera_feed):
    
    _,frame = camera_feed.read()
    #Convert the current frame to HSV
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Define the threshold for finding a blue object with hsv
    lower_blue = np.array([50,150,200])
    upper_blue = np.array([100,210,255])

    #Create a binary image, where anything blue appears white and everything else is black
    mask = cv2.inRange(frame, lower_blue, upper_blue)

    #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    mask = cv2.erode(mask,element, iterations=2)
    mask = cv2.dilate(mask,element,iterations=2)
    mask = cv2.erode(mask,element)
    
    #Create Contours for all blue objects
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
     #Create a bounding box around the biggest blue object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
	location = [(x+w)/2, (y+h)/2]
	print "orange: " + str(location)
	urllib.urlopen("http://54.218.43.192/robot_tag/1/add_coords/" + str(location[0]).zfill(3) + str(location[1]).zfill(3) + "/")

    #Show the original camera feed with a bounding box overlayed 
    cv2.imshow('frame',frame)
    #Show the contours in a seperate window
    cv2.imshow('mask',mask)
    #Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF

def track_green(camera_feed):
    
    _,frame = camera_feed.read()
    #Convert the current frame to HSV
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Define the threshold for finding a blue object with hsv
    lower_blue = np.array([130,170,100])
    upper_blue = np.array([190,230,160])

    #Create a binary image, where anything blue appears white and everything else is black
    mask = cv2.inRange(frame, lower_blue, upper_blue)

    #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    mask = cv2.erode(mask,element, iterations=2)
    mask = cv2.dilate(mask,element,iterations=2)
    mask = cv2.erode(mask,element)
    
    #Create Contours for all blue objects
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    #Create a bounding box around the biggest blue object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
	location = [(x+w)/2, (y+h)/2]
	print "orange: " + str(location)
	urllib.urlopen("http://54.218.43.192/robot_tag/2/add_coords/" + str(location[0]).zfill(3) + str(location[1]).zfill(3) + "/")

    #Show the original camera feed with a bounding box overlayed 
    cv2.imshow('frame',frame)
    #Show the contours in a seperate window
    cv2.imshow('mask',mask)
    #Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF

main()

