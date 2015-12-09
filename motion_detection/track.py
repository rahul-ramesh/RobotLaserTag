#Import OpenCV
import cv2
#Import Numpy
import numpy as np
import urllib

def main():

    camera_feed = cv2.VideoCapture(0)

    while(1):

	_,frame = camera_feed.read()

	orange_box = track_orange(frame)
	green_box = track_green(frame)

        cv2.rectangle(frame, (orange_box[0],orange_box[1]),(orange_box[0] + orange_box[2],orange_box[1] + orange_box[3]), (0,0,255), 3)
	cv2.rectangle(frame, (green_box[0],green_box[1]),(green_box[0] + green_box[2],green_box[1] + green_box[3]), (0,0,255), 3)

	#Show the original camera feed with a bounding box overlayed 
	#cv2.imshow('frame',frame)

    	#If escape is pressed close all windows
        k = cv2.waitKey(5) & 0xFF
    	if k == 27:
    	    break

    cv2.destroyAllWindows()

def track_orange(frame):
    
    
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
    [x,y,w,h] = [0,0,0,0]
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        location = [(x+w)/2, (y+h)/2]
	print "orange: " + str(location)
	urllib.urlopen("http://54.218.43.192/robot_tag/1/add_coords/" + str(location[0]).zfill(3) + str(location[1]).zfill(3) + "/")
    return [x,y,w,h]


def track_green(frame):
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
    [x,y,w,h] = [0,0,0,0]
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
	location = [(x+w)/2, (y+h)/2]
	print "orange: " + str(location)
	urllib.urlopen("http://54.218.43.192/robot_tag/2/add_coords/" + str(location[0]).zfill(3) + str(location[1]).zfill(3) + "/")
    return [x,y,w,h]

main()

