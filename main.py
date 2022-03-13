import pyvirtualcam
import cv2
import platform
import os

verbose = True

# capture = cv2.VideoCapture('http://192.168.43.251:8080/video')
capture = cv2.VideoCapture('./sample_video.mp4')

width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
fps = int(capture.get(cv2.CAP_PROP_FPS))  # float `fps`
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # float `frame count`

print(platform.system())
if platform.system() == "Linux":
    os.system("sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label=\"Virtual\"")
    device = "/dev/video4"
else:
    device = "OBS Virtual Camera"

cam = pyvirtualcam.Camera(width=width, height=height, fps=fps, device=device)

if verbose:
    print('Size: ', width, 'x', height, '\nFPS: ', fps, '\nTotal Frames: ', frame_count, sep='')

while True:
    ret, frame = capture.read()
    if (cv2.waitKey(1) & 0xFF == ord('q')) or not ret:
        break
    # cv2.putText(frame, 'TEST', (width - 320, height - 120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # this line corrects the color coding
    cam.send(frame)

capture.release()
cv2.destroyAllWindows()
