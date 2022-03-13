import pyvirtualcam
import cv2


verbose = True

# capture = cv2.VideoCapture('http://192.168.43.251:8080/video')
capture = cv2.VideoCapture('./2018510062_Uygar_Uygun_LAB3_Video.mp4')

width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
fps = int(capture.get(cv2.CAP_PROP_FPS))  # float `fps`
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # float `frame count`

cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)


if verbose:
    print('Size: ', width, 'x', height, '\nFPS: ', fps, '\nTotal Frames: ', frame_count, sep='')


while True:
    ret, frame = capture.read()
    if (cv2.waitKey(1) & 0xFF == ord('q')) or not ret:
        break
    # cv2.putText(frame, 'TEST', (width - 320, height - 120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #this line corrects the color coding
    cam.send(frame)

capture.release()
cv2.destroyAllWindows()
