import sys

from cv2 import VideoCapture, flip, setLogLevel, VideoWriter_fourcc
from cv2 import CAP_V4L2, CAP_DSHOW, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FOURCC, CAP_PROP_BACKEND
from PySide6.QtMultimedia import QMediaDevices, QVideoFrameFormat
import Preview


class MovenetWidget(Preview.PreviewWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.changeBtn.hide()

	class Thread(Preview.PreviewWidget.Thread):
		movenet_frame = -1

		def __init__(self, parent, previewSize, outputCamera):
			super().__init__(parent, previewSize)

		def run(self):
			self.ThreadActive = True

		def updateFrameSlot(self, frame):
			self.movenet_frame = (self.movenet_frame + 1) % 10
			if self.movenet_frame == 0:
				# TODO PROCESS HERE

				self.updateFrame.emit(frame)

