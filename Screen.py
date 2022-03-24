from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, Qt

import cv2
from mss import mss
from numpy import array as np_array

import Preview


class ScreenWidget(Preview.PreviewWidget):
	def __init__(self, parent=None, verbose=False):
		super().__init__(parent, verbose)

	class Thread(Preview.PreviewWidget.Thread):
		updateFrame = Signal(QImage)
		mon = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}

		def __init__(self, parent=None):
			super().__init__(parent)

		def run(self):
			self.ThreadActive = True
			scrCapt = mss()  # Screen capturing utility
			while self.ThreadActive:
				frame = scrCapt.grab(self.mon)
				ret = (frame is not None)
				if ret:
					Image = cv2.cvtColor(np_array(frame), cv2.COLOR_BGR2RGB)
					FlippedImage = Image
					ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
					Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
					self.updateFrame.emit(Pic)
