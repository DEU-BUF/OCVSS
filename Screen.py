from PySide6.QtGui import QScreen, QGuiApplication
from mss import mss
from numpy import array as np_array
import Preview


class ScreenWidget(Preview.PreviewWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.changeBtn.setText("Change Screen")

	class Thread(Preview.PreviewWidget.Thread):

		def __init__(self, parent, previewSize):
			super().__init__(parent, previewSize)
			self.screens = QGuiApplication.screens()

		def source(self):
			return mss()

		def getFrame(self, source):
			geo = self.screens[self.inputIndex].geometry()
			mon = {"top": geo.y(), "left": geo.x(), "width": geo.width(), "height": geo.height()}
			frame = source.grab(mon)
			ret = (frame is not None)
			return ret, frame

		def usableFrame(self, frame):
			return np_array(frame)

		def changeInputSource(self):
			self.inputIndex = (self.inputIndex + 1) % len(self.screens)

