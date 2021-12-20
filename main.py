import cv2
from pyvirtualdisplay import Display
import os

verbose = True

# capture = cv2.VideoCapture('http://192.168.43.251:8080/video')
capture = cv2.VideoCapture('./sample_video.mp4')

width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
fps = int(capture.get(cv2.CAP_PROP_FPS))  # float `fps`
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # float `frame count`

if verbose:
    print('Size: ', width, 'x', height, '\nFPS: ', fps, '\nTotal Frames: ', frame_count, sep='')

print(os.environ["DISPLAY"])

disp = Display(backend="xvfb", size=(width, height))
# disp = Display(backend="xephyr", size=(width, height))
# disp = Display(backend="xvnc", size=(width, height))

disp.start()
os.environ["DISPLAY"] = ':0'
print(os.environ["DISPLAY"])

cv2.namedWindow("frame", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)
while True:
    ret, frame = capture.read()
    if (cv2.waitKey(1) & 0xFF == ord('q')) or not ret:
        break
    cv2.putText(frame, 'TEST', (width - 320, height - 120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0))
    cv2.imshow('frame', frame)

disp.stop()
capture.release()
cv2.destroyAllWindows()
