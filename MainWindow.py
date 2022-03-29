import sys

from PySide6.QtCore import QMetaObject, QCoreApplication
from PySide6.QtGui import QMovie, QPixmap, QImage
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QMainWindow, QLabel, QSizePolicy, QStyleFactory
from PySide6 import __version__

import Camera
import VideoInput
import Screen

verbose = True
CameraInput = False

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(1120, 449)

		self.centralWidget = QWidget(self)
		self.gridLayout = QGridLayout(self.centralWidget)

		self.stopBtn = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.stopBtn, 2, 0, 1, 1)

		self.startBtn = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.startBtn, 2, 1, 1, 1)

		# Create camera and screen widgets and add to the layout
		if CameraInput:
			self.cameraWidget = Camera.CameraWidget(self.centralWidget)
			self.gridLayout.addWidget(self.cameraWidget, 0, 0, 1, 1)
		else:
			self.videoInputWidget = VideoInput.VideoInputWidget(self.centralWidget)
			self.gridLayout.addWidget(self.videoInputWidget, 0, 0, 1, 1)

		self.screenWidget = Screen.ScreenWidget(self.centralWidget)
		self.gridLayout.addWidget(self.screenWidget, 0, 1, 1, 1)

		self.setCentralWidget(self.centralWidget)

		self.retranslateUi(self)

		QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, Window):
		Window.setWindowTitle(QCoreApplication.translate("MainWindow", "OCVSS", None))
		self.stopBtn.setText(QCoreApplication.translate("MainWindow", "STOP OCVSS", None))
		self.startBtn.setText(QCoreApplication.translate("MainWindow", "START OCVSS", None))


if __name__ == "__main__":
	print("Qt version:", __version__.__str__())
	app = QApplication(sys.argv)

	print("Available styles:")
	styles = QStyleFactory.keys()
	for s in styles:
		print("   ", s)
	print("\nSelected:", app.style().name())

	widget = MainWindow()
	widget.resize(800, 600)
	widget.show()

	if CameraInput:
		app.aboutToQuit.connect(widget.cameraWidget.stopPreviewFeed)
	else:
		app.aboutToQuit.connect(widget.videoInputWidget.stopPreviewFeed)
	app.aboutToQuit.connect(widget.screenWidget.stopPreviewFeed)

	sys.exit(app.exec())
