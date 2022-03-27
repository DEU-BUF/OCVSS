import sys

from cv2 import VideoCapture, flip, setLogLevel, VideoWriter_fourcc
from cv2 import CAP_V4L2, CAP_DSHOW, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FOURCC
from PySide6.QtMultimedia import QMediaDevices
import Preview

KNOWN_FOURCC_VALUES = {"YUYV": 1448695129, "MJPG": 1196444237, "YU12": 1498755378}


class CameraWidget(Preview.PreviewWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.changeBtn.setText("Change Camera")

	class Thread(Preview.PreviewWidget.Thread):
		cameraFormats = []

		def __init__(self, parent, previewSize):
			setLogLevel(0)  # Disable OpenCV logs about gstreamer
			super().__init__(parent, previewSize)

			# Selecting first working camera
			for i in range(10):
				if self.testCamera(i):
					self.inputIndex = i
					break

			# Getting all video resolution x fps x fourccVal combos to brute force later
			for dev in QMediaDevices.videoInputs():
				for vidForm in dev.videoFormats():
					fps = vidForm.maxFrameRate()
					if fps < 23:
						continue
					width = vidForm.resolution().width()
					height = vidForm.resolution().height()
					bitrate = width * height * fps
					fourccVal = str(vidForm.pixelFormat().name).split('_')[1][:-1].upper()
					# Exception in naming
					if fourccVal == "JPEG":
						fourccVal = "MJPG"
					fourcc = VideoWriter_fourcc(fourccVal[0], fourccVal[1], fourccVal[2], fourccVal[3])

					device = {"bitrate": bitrate, "fps": vidForm.maxFrameRate(), "width": vidForm.resolution().width(), "height": vidForm.resolution().height(), "fourcc": fourcc}
					self.cameraFormats.append(device)

			self.cameraFormats = sorted(self.cameraFormats, key=lambda x: -x["bitrate"])

		def source(self):
			if sys.platform == "win32":
				cap = VideoCapture(self.inputIndex, CAP_DSHOW)
				self.setMaxBitrate(cap)
				return cap
			elif sys.platform == "linux":
				cap = VideoCapture(self.inputIndex, CAP_V4L2)
				# cap.read() # WAIT UNTIL CAMERA IS READY
				self.setMaxBitrate(cap)
				return cap

		def setMaxBitrate(self, source):
			for prop in self.cameraFormats:
				source.set(CAP_PROP_FPS, prop["fps"])
				source.set(CAP_PROP_FRAME_WIDTH, prop["width"])
				source.set(CAP_PROP_FRAME_HEIGHT, prop["height"])
				source.set(CAP_PROP_FOURCC, prop["fourcc"])

				# Wait for a frame to come
				ret, _ = source.read()
				# If the just tried values are set correctly
				if ret and source.get(CAP_PROP_FRAME_WIDTH) == prop["width"] and source.get(CAP_PROP_FRAME_HEIGHT) == prop["height"] and source.get(CAP_PROP_FPS) == prop["fps"] and source.get(CAP_PROP_FOURCC) == prop["fourcc"]:
					break

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
