import sys

from cv2 import VideoCapture, flip, setLogLevel, VideoWriter_fourcc
from PySide6.QtMultimedia import QMediaDevices, QVideoFrameFormat
import Preview

KNOWN_FOURCC_VALUES = {"YUYV": 1448695129, "MJPG": 1196444237, "YU12": 1498755378}


class VideoInputWidget(Preview.PreviewWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.changeBtn.setText("Change Video Input")

	class Thread(Preview.PreviewWidget.Thread):

		def __init__(self, parent, previewSize):
			super().__init__(parent, previewSize)

		def source(self):
			return VideoCapture("sample_video.mp4")

		def getFrame(self, source):
			return source.read()

		def changeInputSource(self):
			pass
