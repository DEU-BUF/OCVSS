import pyvirtualcam
from mss import mss
from numpy import array as np_array
import cv2
import platform
import time
import os
import sys

from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FOURCC

import tensorflow as tf
from TensorHelper import *

cameraOut = False

width = height = fps = frame_count = 0

# tf
input_size = 192


def main():
	if sys.platform == "win32":
		capture = cv2.VideoCapture(1)
	elif sys.platform == "linux":
		capture = cv2.VideoCapture("media/class_video2_720_30fps.mp4")

	capture.set(CAP_PROP_FPS, 30)
	capture.set(CAP_PROP_FRAME_WIDTH, 1280)
	capture.set(CAP_PROP_FRAME_HEIGHT, 720)
	capture.set(CAP_PROP_FOURCC, 1196444237)
	capture.read()

	getInputProperties(capture)
	cam = cameraOutput()

	print('Size: ', width, 'x', height, '\nFPS: ', fps, '\nTotal Frames: ', frame_count, sep='')

	# tf
	interpreter = tf.lite.Interpreter(model_path="model.tflite")
	interpreter.allocate_tensors()

	def movenet(input_image):
		# TF Lite format expects tensor type of uint8.
		input_image = tf.cast(input_image, dtype=tf.uint8)
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()
		interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
		# Invoke inference.
		interpreter.invoke()
		# Get the model prediction.
		keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
		f = open("keypoints.txt", "w")
		f.write(str(input_details[0]))
		f.write("\n")
		f.write(str(output_details[0]))
		f.close()
		return keypoints_with_scores

	# Main loop
	try:
		while True:
			retVal, frame = capture.read()

			if (cv2.waitKey(1) & 0xFF == ord('q')) or not retVal:
				break

			if cameraOut:
				frame = cv2.cvtColor(np_array(frame), cv2.COLOR_RGB2BGR)  # this line corrects the color coding
				cam.send(frame)
			else:
				frame = cv2.flip(frame, 1)

				input_frame = tf.expand_dims(frame, axis=0)
				input_frame = tf.image.resize_with_pad(input_frame, input_size, input_size)

				keypoints_with_scores = movenet(input_frame)


				display_image = tf.expand_dims(frame, axis=0)
				display_image = tf.cast(tf.image.resize_with_pad(
					display_image, 1280, 1280), dtype=tf.int32)
				output_overlay = draw_prediction_on_image(
					np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)
				cv2.imshow('frame', output_overlay)


	except KeyboardInterrupt:
		pass

	# Exiting
	cv2.destroyAllWindows()
	capture.release()
	if cameraOut:
		showPlaceholder(cam)
		cam.close()
		if platform.system() == "Linux":
			retVal = -1
			while retVal != 0:
				if retVal != -1:
					time.sleep(1)
				retVal = os.system("sudo modprobe -r v4l2loopback")


def getInputProperties(capture):
	global width, height, fps, frame_count
	width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
	height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
	fps = int(capture.get(cv2.CAP_PROP_FPS))  # float `fps`
	frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # float `frame count`


def cameraOutput():
	if cameraOut:
		if platform.system() == "Linux":
			os.system("sudo modprobe v4l2loopback devices=1 video_nr=4 card_label=\"OCVSS\" exclusive_caps=1")
			device = "/dev/video4"
			time.sleep(0.1)
		elif platform.system() == "Darwin":
			device = "unknown"  # for some reason Mac is named Darwin
		else:
			device = "OBS Virtual Camera"

		return pyvirtualcam.Camera(width, height, fps, device=device)
	else:
		cv2.namedWindow("frame", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)


def showPlaceholder(cam):
	ph = cv2.imread("media/placeholder.png")
	ph = cv2.cvtColor(ph, cv2.COLOR_RGB2BGR)
	ph = cv2.resize(ph, (width, height))
	for i in range(fps):
		cam.send(ph)


if __name__ == '__main__':
	main()
