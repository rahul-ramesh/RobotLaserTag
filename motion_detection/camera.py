import cv2
cam = cv2.VideoCapture(0)
s, img = cam.read()

winName = "Quadcopter Tracker"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

while s:
    cv2.imshow( winName,img )

    s, img = cam.read()

    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyWindow(winName)
        break


print "Goodbye"

