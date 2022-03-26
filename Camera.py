import sys

import cv2
from cv2.cv2 import VideoCapture, flip, setLogLevel, videoio_registry
from PySide6.QtMultimedia import QMediaDevices
import Preview

KNOWN_FOURCC_VALUES = {"YUYV": 1448695129, "MJPG": 1196444237, "YU12": 1498755378}


class CameraWidget(Preview.PreviewWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.changeBtn.setText("Change Camera")

	for dev in QMediaDevices.videoInputs():
		print(dev.description())
		print(dev.id())
		print(dev.isNull())
		for vidForm in dev.videoFormats():
			print(vidForm.resolution().width(), vidForm.resolution().height(), vidForm.maxFrameRate(), str(vidForm.pixelFormat().name).split('_')[1][:4])

	class Thread(Preview.PreviewWidget.Thread):

		def __init__(self, parent, previewSize):
			# setLogLevel(0)  # Disable OpenCV logs about gstreamer
			super().__init__(parent, previewSize)

			#Selecting first working camera
			for i in range(10):
				if self.testCamera(i):
					self.inputIndex = i
					break

		def source(self):
			if sys.platform == "win32":
				cap = VideoCapture(self.inputIndex, cv2.CAP_DSHOW)
				cap.set(cv2.CAP_PROP_FPS, 30.0)
				cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280.0)
				cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720.0)
				#cap.set(cv2.CAP_PROP_FOURCC, )
				print(cap.get(cv2.CAP_PROP_FPS))
				print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
				print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
				print(cap.get(cv2.CAP_PROP_FOURCC))
				print(cap.get(cv2.CAP_PROP_BACKEND))
				return cap
			elif sys.platform == "linux":
				cap = VideoCapture(self.inputIndex, cv2.CAP_GSTREAMER)#, cv2.CAP_V4L2)
				print(cap.get(cv2.CAP_PROP_FPS))
				# cap.set(cv2.CAP_PROP_FPS, 30.0)
				print(cap.get(cv2.CAP_PROP_FPS))

				print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
				cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280.0)
				print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

				print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
				cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720.0)
				print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

				print(cap.get(cv2.CAP_PROP_FOURCC))
				cap.set(cv2.CAP_PROP_FOURCC, 1196444237)
				print(cap.get(cv2.CAP_PROP_FOURCC))

				print("")
				print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
				print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
				print(cap.get(cv2.CAP_PROP_FPS))
				print(cap.get(cv2.CAP_PROP_FOURCC))
				return cap

		def getFrame(self, source):
			return source.read()

		def flip(self, frame):
			return flip(frame, 1)

		def changeInputSource(self):
			for i in range(1, 10):
				if self.testCamera((self.inputIndex + i) % 10):
					self.inputIndex = (self.inputIndex + i) % 10
					break

		def testCamera(self, index):
			testCameraSource = VideoCapture(index)
			ret, _ = testCameraSource.read()
			return ret