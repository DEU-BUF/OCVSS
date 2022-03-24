from PySide6.QtGui import Qt, QImage
from PySide6.QtCore import Signal

import cv2

import Preview


class CameraWidget(Preview.PreviewWidget):
	def __init__(self, parent=None, verbose=False):
		super().__init__(parent, verbose)

	class Thread(Preview.PreviewWidget.Thread):
		updateFrame = Signal(QImage)

		def __init__(self, parent=None):
			super().__init__(parent)

		def run(self):
			self.ThreadActive = True
			Capture = cv2.VideoCapture(0)
			while self.ThreadActive:
				ret, frame = Capture.read()
				if ret:
					Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					FlippedImage = cv2.flip(Image, 1)
					ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
					Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
					self.updateFrame.emit(Pic)
