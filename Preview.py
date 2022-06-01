import numpy
from PySide6.QtGui import Qt, QImage, QPixmap, QMovie, QColor
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QFrame, QGridLayout, QPushButton
from PySide6.QtCore import QThread, Signal, QSize

from cv2 import cvtColor, COLOR_BGR2RGB
from abc import abstractmethod


class PreviewWidget(QWidget):
	previewSize = QSize(640, 360)

	def __init__(self, parent=None, outputCamera=None):
		super().__init__(parent)

		self.layout = QGridLayout()
		self.setLayout(self.layout)

		self.previewView = QLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.previewView.sizePolicy().hasHeightForWidth())
		self.previewView.setSizePolicy(sizePolicy)
		self.previewView.setMinimumSize(self.previewSize)
		self.previewView.setFrameShape(QFrame.Box)
		self.previewView.setFrameShadow(QFrame.Raised)
		self.previewView.setLineWidth(3)
		self.previewView.setAlignment(Qt.AlignCenter)
		self.loading()
		self.layout.addWidget(self.previewView, 0, 0, 1, 1)

		self.previewThread = self.Thread(self, self.previewView, outputCamera)
		self.previewThread.start()
		self.previewThread.updateFrame.connect(self.updateFrameSlot)

		self.changeBtn = QPushButton("Change")
		self.changeBtn.clicked.connect(self.changeInputSource)
		self.layout.addWidget(self.changeBtn, 1, 0, 1, 1)


	def updateFrameSlot(self, image):
		self.previewView.setPixmap(QPixmap.fromImage(image))

	def startPreviewFeed(self):
		self.previewThread.start()

	def stopPreviewFeed(self):
		self.previewThread.stop()
		self.previewThread.wait()

	def changeInputSource(self):
		self.previewThread.updateFrame.disconnect(self.updateFrameSlot)

		self.loading()

		self.stopPreviewFeed()
		self.previewThread.changeInputSource()
		self.previewThread.updateFrame.connect(self.updateFrameSlot)
		self.startPreviewFeed()

	def loading(self):
		loadingGIF = QMovie("media/loading.gif")
		self.previewView.setMovie(loadingGIF)
		loadingGIF.start()


	class Thread(QThread):
		updateFrame = Signal(QImage)
		updateFrameNP = Signal(numpy.ndarray)
		ThreadActive = False
		inputIndex = 0

		def __init__(self, parent, previewSize, outputCamera=None):
			super().__init__(parent)
			self.previewSize = previewSize
			self.cam = outputCamera

		def run(self):

			self.ThreadActive = True
			frameSource = self.source()
			while self.ThreadActive:
				ret, frame = self.getFrame(frameSource)
				if not ret:
					continue
				self.updateFrameNP.emit(frame)
				colorCorrectedFrame = cvtColor(self.usableFrame(frame), COLOR_BGR2RGB)
				flippedFrame = self.flip(colorCorrectedFrame)
				frameInQtFormat = QImage(flippedFrame.data, flippedFrame.shape[1], flippedFrame.shape[0], QImage.Format_RGB888)
				finalFrame = frameInQtFormat.scaled(self.previewSize.width(), self.previewSize.height(), Qt.KeepAspectRatio)
				self.updateFrame.emit(finalFrame)

		@abstractmethod
		def source(self):
			pass

		@abstractmethod
		def getFrame(self, source):
			pass

		def usableFrame(self, frame):
			return frame

		def flip(self, frame):
			return frame

		@abstractmethod
		def changeInputSource(self):
			pass

		def stop(self):
			self.ThreadActive = False
			self.quit()
