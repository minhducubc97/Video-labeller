from imutils.video import VideoStream
import argparse # parse arguments
import imutils # a module specificly used to resize, rotate and crop images
import time
import cv2
import os
import shutil

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser() 	# Specially designed for command line string
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="csrt", help="OpenCV object tracker type")
ap.add_argument("-a", "--annot", type=str, help="Annotation file")
args = vars(ap.parse_args())	# vars() return a dictionary, which means args is a dictionary

# calculate xmin, xmax, ymin, ymax
def calBoundingBox(x, y, w, h):
	xmin = 0
	ymin = 0
	xmax = 0
	ymax = 0
	
	if (x < 0):
		xmin = 0
	elif (x > w):
		xmin = w
	else:
		xmin = x
	if (x + w < 0):
		xmax = 0
	elif (x + w > w):
		xmax = w
	else:
		xmax = x + w
	if (y < 0):
		ymin = 0
	elif (y > h):
		ymin = h
	else:
		ymin = y
	if (y + h < 0):
		ymax = 0
	elif (y + h > h):
		ymax = h
	else:
		ymax = y + h
	return xmin, xmax, ymin, ymax

# clear all files in folder
def clearFolder(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

# Initialize a dictionary that maps strings to their corresponding OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	# NOTE: These are 8 types of tracker, by default csrt is chosen. These functions sometimes go missing in the official distribution, so in these cases, to solve the problem, install opencv-contrib: pip install opencv-contrib-python
	"csrt": cv2.TrackerCSRT_create,                  	# RECOMMENDED: A bit slow but very accurate
	"kcf": cv2.TrackerKCF_create,                     	# RECOMMENDED: Averagely fast and averagely accurate
	"boosting": cv2.TrackerBoosting_create,				# Slow and not very accurate (and the oldest)
	"mil": cv2.TrackerMIL_create,						# Averagely accurate, but handle errors badly
	"tld": cv2.TrackerTLD_create,						# NOT RECOMMENDED: Prone to false-positive
	"medianflow": cv2.TrackerMedianFlow_create,			# Doesn't work well when there is a sudden change in motion
	"mosse": cv2.TrackerMOSSE_create,				  	# RECOMMENDED: Extremely fast but not very accurate -> good when user needs for speed
	"goturn": cv2.TrackerGOTURN_create					# Complicated
}

widthVal = 720
heightVal = 540
trackers = cv2.MultiTracker_create()
vs = cv2.VideoCapture(args["video"])
counter = 0
txtfile = open(args.get("annot"), 'w')
startSelecting = True
videoName = args["video"].split('\\')[-1].split('.')[0]

# clear the frames folder
clearFolder('frames/')
# loop over frames from the video stream
while True:
	counter += 1
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame

	# check to see if we have reached the end of the stream
	if frame is None:
		break

	# resize the frame (so we can process it faster)
	frame = imutils.resize(frame, width=widthVal, height=heightVal)
	cv2.imwrite('frames/' + videoName + "-" + str(counter).zfill(3) + '.png', frame)

	# get the keyboard input
	key = cv2.waitKey(1) & 0xFF

	if (startSelecting == True):
		# select the bounding box of the object we want to track (make sure you press ENTER or SPACE after selecting the ROI)
		boxes = cv2.selectROIs("Frame", frame, fromCenter=False, showCrosshair=True) 
		boxes = tuple(map(tuple, boxes))
		
		for box in boxes:
			# create a new object tracker for the bounding box and add it to our multi-object tracker
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)
		startSelecting = False

	# grab the updated bounding box coordinates (if any) for each object that is being tracked
	(success, boxes) = trackers.update(frame)

	# loop over the bounding boxes
	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]

		# draw to frame
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		# write to file
		xmin, xmax, ymin, ymax = calBoundingBox(x, y, w, h)
		txtfile.write('frame:' + str(counter).zfill(3) + ',xmin:' + str(xmin) + ',xmax:' + str(xmax) + ',ymin:' + str(ymin) + ',ymax:' + str(ymax) + '\n')

	# show the output frame
	cv2.imshow("Frame", frame)

	# press 'c' key, redraw bounding boxes
	if key == ord("c"):
		trackers.clear()
		trackers = cv2.MultiTracker_create()
		(success, boxes) = trackers.update(frame)
		boxes = cv2.selectROIs("Frame", frame, fromCenter=False, showCrosshair=True) 
		boxes = tuple(map(tuple, boxes))
		
		for box in boxes:
			# create a new object tracker for the bounding box and add it to our multi-object tracker
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)

	# press 'r' key, all bounding boxes will be removed
	elif key == ord("r"):
		trackers.clear()
		trackers = cv2.MultiTracker_create()
		(success, boxes) = trackers.update(frame)

	# press 'q' key, break from the loop
	elif key == ord("q"):
		break

txtfile.close()
vs.release()

# close all windows
cv2.destroyAllWindows()