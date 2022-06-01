import numpy as np
from PySide6.QtCore import QMetaObject, QCoreApplication, QThread, Signal, QSize
from PySide6.QtGui import QMovie, QPixmap, QImage, Qt
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QMainWindow, QLabel, QSizePolicy, QStyleFactory, QFrame

import pyvirtualcam
from mss import mss
from numpy import array as np_array
import cv2
import platform
import time
import os
import sys

from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FOURCC, CAP_V4L2

import tensorflow as tf
from TensorHelper import *

width = height = fps = frame_count = 0

# tf
input_size = 192


class PreviewThread(QThread):
	kameradanFrameGeldiGitEkranaBas = Signal(QImage)
	kameradanFrameGeldigitMovenetIsle = Signal(np.ndarray)
	ThreadActive = False
	inputIndex = 0

	def __init__(self, parent, previewSize):
		super().__init__(parent)
		self.previewSize = previewSize

	def run(self):
		self.ThreadActive = True
		frameSource = self.source()
		while self.ThreadActive:
			ret, frame = self.getFrame(frameSource)
			if not ret:
				continue

			self.kameradanFrameGeldigitMovenetIsle.emit(frame) # <class 'numpy.ndarray'>

			colorCorrectedFrame = cv2.cvtColor(self.usableFrame(frame), cv2.COLOR_BGR2RGB)
			flippedFrame = self.flip(colorCorrectedFrame)

			frameInQtFormat = QImage(flippedFrame.data, flippedFrame.shape[1], flippedFrame.shape[0], QImage.Format_RGB888)
			finalFrame = frameInQtFormat.scaled(self.previewSize.width(), self.previewSize.height(), Qt.KeepAspectRatio)
			self.kameradanFrameGeldiGitEkranaBas.emit(finalFrame) # <class 'PySide6.QtGui.QImage'>

	def source(self):
		if sys.platform == "win32":
			capture = cv2.VideoCapture(1)
		elif sys.platform == "linux":
			# capture = cv2.VideoCapture("media/class_video2_720_30fps.mp4")
			capture = cv2.VideoCapture(0, CAP_V4L2)

		capture.set(CAP_PROP_FPS, 30)
		capture.set(CAP_PROP_FRAME_WIDTH, 1280)
		capture.set(CAP_PROP_FRAME_HEIGHT, 720)
		capture.set(CAP_PROP_FOURCC, 1196444237)
		capture.read()

		getInputProperties(capture)
		print('Size: ', width, 'x', height, '\nFPS: ', fps, '\nTotal Frames: ', frame_count, sep='')

		return capture

	def getInputProperties(capture):
		global width, height, fps, frame_count
		width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
		height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
		fps = int(capture.get(cv2.CAP_PROP_FPS))  # float `fps`
		frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # float `frame count`

	def getFrame(self, source):
		return source.read()

	def usableFrame(self, frame):
		return frame

	def flip(self, frame):
		# return cv2.flip(frame, 1)
		return frame

	def stop(self):
		self.ThreadActive = False
		self.quit()


def movenet(input_image, interpreter):
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


class movenetThread(QThread):
	movenettenFrameGeldi = Signal(QImage)
	ThreadActive = False
	inputIndex = 0
	movenet_frame = -1

	def __init__(self, parent, previewSize):
		super().__init__(parent)
		self.previewSize = previewSize
		self.interpreter = tf.lite.Interpreter(model_path="model.tflite")
		self.interpreter.allocate_tensors()

	def run(self):
		self.ThreadActive = True

	def movenetFrameiIsleSlot(self, frame):
		self.movenet_frame = (self.movenet_frame + 1) % 10
		if self.movenet_frame == 0:

			input_frame = tf.expand_dims(frame, axis=0)
			input_frame = tf.image.resize_with_pad(input_frame, input_size, input_size)

			keypoints_with_scores = movenet(input_frame, self.interpreter)

			display_image = tf.expand_dims(frame, axis=0)
			display_image = tf.cast(tf.image.resize_with_pad(display_image, 1280, 1280), dtype=tf.int32)
			output_overlay = draw_prediction_on_image(np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

			colorCorrectedFrame = cv2.cvtColor(np_array(output_overlay), cv2.COLOR_BGR2RGB)

			frameInQtFormat = QImage(colorCorrectedFrame.data, colorCorrectedFrame.shape[1], colorCorrectedFrame.shape[0],
			                         QImage.Format_RGB888)
			finalFrame = frameInQtFormat.scaled(self.previewSize.width(), self.previewSize.height(), Qt.KeepAspectRatio)

			self.movenettenFrameGeldi.emit(finalFrame)


	def stop(self):
		self.ThreadActive = False
		self.quit()

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

class MainWindow(QMainWindow):
	previewSize = QSize(853, 480)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(self.previewSize.width() * 2, self.previewSize.height())

		self.centralWidget = QWidget()
		self.layout = QGridLayout()
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)

		self.previewWidget = QLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.previewWidget.sizePolicy().hasHeightForWidth())
		self.previewWidget.setSizePolicy(sizePolicy)
		self.previewWidget.setMinimumSize(self.previewSize)
		self.previewWidget.setFrameShape(QFrame.Box)
		self.previewWidget.setFrameShadow(QFrame.Raised)
		self.previewWidget.setLineWidth(3)
		self.previewWidget.setAlignment(Qt.AlignCenter)
		self.loading()
		self.layout.addWidget(self.previewWidget, 0, 0)

		self.previewThread = PreviewThread(self, self.previewWidget)
		self.previewThread.start()
		self.previewThread.kameradanFrameGeldiGitEkranaBas.connect(self.SoldakiFrameeResmiBasSlot)


		self.movenetWidget = QLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.movenetWidget.sizePolicy().hasHeightForWidth())
		self.movenetWidget.setSizePolicy(sizePolicy)
		self.movenetWidget.setMinimumSize(self.previewSize)
		self.movenetWidget.setFrameShape(QFrame.Box)
		self.movenetWidget.setFrameShadow(QFrame.Raised)
		self.movenetWidget.setLineWidth(3)
		self.movenetWidget.setAlignment(Qt.AlignCenter)
		self.loading()
		self.layout.addWidget(self.movenetWidget, 0, 1)

		self.movenetThread = movenetThread(self, self.movenetWidget)
		self.movenetThread.start()
		self.movenetThread.movenettenFrameGeldi.connect(self.SagdakiFrameeResmiBasSlot)

		self.previewThread.kameradanFrameGeldigitMovenetIsle.connect(self.movenetThread.movenetFrameiIsleSlot)

	def SoldakiFrameeResmiBasSlot(self, image):
		self.previewWidget.setPixmap(QPixmap.fromImage(image))

	def SagdakiFrameeResmiBasSlot(self, image):
		self.movenetWidget.setPixmap(QPixmap.fromImage(image))

	def startPreviewFeed(self):
		self.previewThread.start()
		self.movenetThread.start()

	def stopPreviewFeed(self):
		self.previewThread.stop()
		self.movenetThread.stop()

		self.previewThread.wait()
		self.movenetThread.wait()

	def loading(self):
		loadingGIF = QMovie("media/loading.gif")
		self.previewWidget.setMovie(loadingGIF)
		loadingGIF.start()

if __name__ == '__main__':
	app = QApplication(sys.argv)

	widget = MainWindow()
	widget.show()

	app.aboutToQuit.connect(widget.stopPreviewFeed)

	sys.exit(app.exec())
