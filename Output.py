import sys
import pyvirtualcam
import platform
import os
import time
import cv2
from numpy import array as np_array

from cv2 import VideoCapture, flip, setLogLevel, VideoWriter_fourcc
from cv2 import CAP_V4L2, CAP_DSHOW, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FOURCC, CAP_PROP_BACKEND
from PySide6.QtMultimedia import QMediaDevices, QVideoFrameFormat
import Preview


class OutputWidget(Preview.PreviewWidget):

	def __init__(self, parent=None):
		if platform.system() == "Linux":
			os.system("sudo modprobe v4l2loopback devices=1 video_nr=4 card_label=\"OCVSS\" exclusive_caps=1")
			device = "/dev/video4"
			time.sleep(0.1)
		elif platform.system() == "Darwin":
			device = "unknown"  # for some reason Mac is named Darwin
		else:
			device = "OBS Virtual Camera"

		#TODO Make the resolution selectible
		self.cam = pyvirtualcam.Camera(1280, 720, 30, device=device)
		super().__init__(parent, self.cam)
		self.changeBtn.hide()

	def createThread(self):
		return self.Thread(self, self.previewSize, outputCamera)

	def showPlaceholder(self):
		ph = cv2.imread("media/placeholder.png")
		ph = cv2.cvtColor(ph, cv2.COLOR_RGB2BGR)
		ph = cv2.resize(ph, (1280, 720))
		for i in range(30):
			self.cam.send(ph)

	def stopPreviewFeed(self):
		self.showPlaceholder()
		self.cam.close()
		if platform.system() == "Linux":
			retVal = -1
			while retVal != 0:
				if retVal != -1:
					time.sleep(1)
				retVal = os.system("sudo modprobe -r v4l2loopback")
		super().stopPreviewFeed()

	class Thread(Preview.PreviewWidget.Thread):

		def __init__(self, parent, previewSize, outputCamera):
			super().__init__(parent, previewSize, outputCamera)
			#TODO outputcamera gereksiz galiba, windowsta self.cam ile bu alttaki satır olmadan çalışıyor
			self.cam = outputCamera

		def run(self):
			self.ThreadActive = True

		def updateFrameNPSlot(self, frame):
			frame = np_array(frame)
			frame = cv2.resize(frame, (1280, 720))
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			# print(type(frame))
			# print(frame.shape)
			self.cam.send(frame) # this line corrects the color coding

		def updateFrameSlot(self, frame):
			self.updateFrame.emit(frame)
