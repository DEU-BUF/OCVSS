import pyvirtualcam
from mss import mss
import numpy as np
import cv2

import platform
import time
import os

verbose = True
cameraOut = False
screenCapture = False

mon = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
scrCapt = mss()

# capture = cv2.VideoCapture('http://192.168.5.90:8080/video')
capture = cv2.VideoCapture('./sample_video.mp4')

width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
fps = int(capture.get(cv2.CAP_PROP_FPS))  # float `fps`
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # float `frame count`

if verbose:
    print('Size: ', width, 'x', height, '\nFPS: ', fps, '\nTotal Frames: ', frame_count, sep='')

if cameraOut:
    if platform.system() == "Linux":
        os.system("sudo modprobe v4l2loopback devices=1 video_nr=4 card_label=\"OCVSS\"")
        device = "/dev/video4"
        time.sleep(0.1)
    elif platform.system() == "Darwin":
        device = "unknown"  # for some reason Mac is named Darwin
    else:
        device = "OBS Virtual Camera"

    cam = pyvirtualcam.Camera(width=width, height=height, fps=fps, device=device)
else:
    cv2.namedWindow("frame", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)

# Main loop
try:
    while True:
        if screenCapture:
            frame = scrCapt.grab(mon)
            retVal = (frame != None)
        else:
            retVal, frame = capture.read()

        if (cv2.waitKey(1) & 0xFF == ord('q')) or not retVal:
            break
        #cv2.putText(frame, 'TEST', (width - 320, height - 120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0))
        if cameraOut:
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)  # this line corrects the color coding
            cam.send(frame)
        else:
            cv2.imshow('frame', np.array(frame))
except KeyboardInterrupt:
    pass

# Exiting
cv2.destroyAllWindows()
scrCapt.close()
capture.release()
if cameraOut:
    cam.close()
    if platform.system() == "Linux":
        retVal = -1
        while retVal != 0:
            if retVal != -1:
                time.sleep(1)
            retVal = os.system("sudo modprobe -r v4l2loopback")
