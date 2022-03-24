from PySide2.QtGui import Qt, QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy, QFrame, QGridLayout, QPushButton
from PySide2.QtCore import QSize, QThread, Signal, Slot
import cv2


class CameraWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.layout = QGridLayout()
		self.setLayout(self.layout)

		self.cameraView = QLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.cameraView.sizePolicy().hasHeightForWidth())
		self.cameraView.setSizePolicy(sizePolicy)
		self.cameraView.setMinimumSize(QSize(533, 300))
		self.cameraView.setFrameShape(QFrame.Box)
		self.cameraView.setFrameShadow(QFrame.Raised)
		self.cameraView.setLineWidth(3)
		self.cameraView.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.cameraView, 0, 0, 1, 2)

		self.cameraThread = CameraThread()
		self.cameraThread.start()
		self.cameraThread.updateFrame.connect(self.updateFrameSlot)

		self.startBtn = QPushButton("START")
		self.startBtn.clicked.connect(self.startCameraFeed)
		self.layout.addWidget(self.startBtn, 1, 0, 1, 1)

		self.cancelBtn = QPushButton("CANCEL")
		self.cancelBtn.clicked.connect(self.stopCameraFeed)
		self.layout.addWidget(self.cancelBtn, 1, 1, 1, 1)

	def updateFrameSlot(self, Image):
		self.cameraView.setPixmap(QPixmap.fromImage(Image))

	def startCameraFeed(self):
		print("START")
		self.cameraThread.start()

	def stopCameraFeed(self):
		self.cameraThread.stop()



class CameraThread(QThread):
	updateFrame = Signal(QImage)
	ThreadActive = False

	def __init__(self, parent=None):
		super().__init__(parent)

	def run(self):
		print("RUN")
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

	def stop(self):
		self.ThreadActive = False
		self.quit()
