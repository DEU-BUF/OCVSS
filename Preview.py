from PySide6.QtGui import Qt, QImage, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QFrame, QGridLayout, QPushButton
from PySide6.QtCore import QSize, QThread, Signal


class PreviewWidget(QWidget):
	def __init__(self, parent=None, verbose=False):
		super().__init__(parent)
		self.verbose = verbose

		self.vprint("testtt")

		self.layout = QGridLayout()
		self.setLayout(self.layout)

		self.previewView = QLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.previewView.sizePolicy().hasHeightForWidth())
		self.previewView.setSizePolicy(sizePolicy)
		self.previewView.setMinimumSize(QSize(533, 300))
		self.previewView.setFrameShape(QFrame.Box)
		self.previewView.setFrameShadow(QFrame.Raised)
		self.previewView.setLineWidth(3)
		self.previewView.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.previewView, 0, 0, 1, 2)

		self.previewThread = self.Thread()
		self.previewThread.start()
		self.previewThread.updateFrame.connect(self.updateFrameSlot)

		self.startBtn = QPushButton("START")
		self.startBtn.clicked.connect(self.startPreviewFeed)
		self.layout.addWidget(self.startBtn, 1, 0, 1, 1)

		self.cancelBtn = QPushButton("CANCEL")
		self.cancelBtn.clicked.connect(self.stopPreviewFeed)
		self.layout.addWidget(self.cancelBtn, 1, 1, 1, 1)

	def vprint(self, *args, **kwargs):
		if self.verbose:
			print(str(self.__class__.__module__) + " " + str(self.__class__.__name__), *args, **kwargs)

	def updateFrameSlot(self, image):
		self.previewView.setPixmap(QPixmap.fromImage(image))

	def startPreviewFeed(self):
		self.previewThread.start()

	def stopPreviewFeed(self):
		self.previewThread.stop()
		self.previewThread.wait()

	class Thread(QThread):
		updateFrame = Signal(QImage)
		ThreadActive = False

		def __init__(self, parent=None):
			super().__init__(parent)


		def stop(self):
			self.ThreadActive = False
			self.quit()
