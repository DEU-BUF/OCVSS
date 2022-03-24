from PySide2.QtGui import Qt, QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy, QFrame, QGridLayout, QPushButton
from PySide2.QtCore import QSize, QThread, Signal, Slot
import cv2
from mss import mss
from numpy import array as np_array


class ScreenWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.layout = QGridLayout()
		self.setLayout(self.layout)

		self.screenView = QLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.screenView.sizePolicy().hasHeightForWidth())
		self.screenView.setSizePolicy(sizePolicy)
		self.screenView.setMinimumSize(QSize(533, 300))
		self.screenView.setFrameShape(QFrame.Box)
		self.screenView.setFrameShadow(QFrame.Raised)
		self.screenView.setLineWidth(3)
		self.screenView.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.screenView, 0, 0, 1, 2)

		self.cameraThread = ScreenThread()
		self.cameraThread.start()
		self.cameraThread.updateFrame.connect(self.updateFrameSlot)

		self.startBtn = QPushButton("START")
		self.startBtn.clicked.connect(self.startCameraFeed)
		self.layout.addWidget(self.startBtn, 1, 0, 1, 1)

		self.cancelBtn = QPushButton("CANCEL")
		self.cancelBtn.clicked.connect(self.stopCameraFeed)
		self.layout.addWidget(self.cancelBtn, 1, 1, 1, 1)

	def updateFrameSlot(self, Image):
		self.screenView.setPixmap(QPixmap.fromImage(Image))

	def startCameraFeed(self):
		print("START")
		self.cameraThread.start()

	def stopCameraFeed(self):
		self.cameraThread.stop()



class ScreenThread(QThread):
	updateFrame = Signal(QImage)
	ThreadActive = False
	mon = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}

	def __init__(self, parent=None):
		super().__init__(parent)

	def run(self):
		print("RUN")
		self.ThreadActive = True
		scrCapt = mss()  # Screen capturing utility
		while self.ThreadActive:
			frame = scrCapt.grab(self.mon)
			ret = (frame is not None)
			if ret:
				Image = cv2.cvtColor(np_array(frame), cv2.COLOR_BGR2RGB)
				# FlippedImage = cv2.flip(Image, 1)
				FlippedImage = Image
				ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
				Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
				self.updateFrame.emit(Pic)

	def stop(self):
		self.ThreadActive = False
		self.quit()
