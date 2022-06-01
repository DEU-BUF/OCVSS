import sys

from PySide6.QtCore import QMetaObject, QCoreApplication
from PySide6.QtGui import QMovie, QPixmap, QImage
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QMainWindow, QLabel, QSizePolicy, QStyleFactory
from PySide6 import __version__

import Camera
import MovenetWidget
import Output
import VideoInput
import Screen

verbose = True
CameraInput = True


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(1120, 449)

		self.centralWidget = QWidget(self)
		self.gridLayout = QGridLayout(self.centralWidget)

		self.stopBtn = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.stopBtn, 3, 0, 1, 1)

		self.startBtn = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.startBtn, 3, 1, 1, 1)

		# Preview widgets
		self.screenWidget = Screen.ScreenWidget(self.centralWidget)
		self.gridLayout.addWidget(self.screenWidget, 0, 1, 1, 1)


		self.movenetWidget = MovenetWidget.MovenetWidget(self.centralWidget)
		self.gridLayout.addWidget(self.movenetWidget, 1, 0, 1, 1)

		self.outputWidget = Output.OutputWidget(self.centralWidget)
		self.gridLayout.addWidget(self.outputWidget, 1, 1, 1, 1)


		# Create camera and screen widgets and add to the layout
		if CameraInput:
			self.cameraWidget = Camera.CameraWidget(self.centralWidget)
			self.gridLayout.addWidget(self.cameraWidget, 0, 0, 1, 1)
			self.cameraWidget.previewThread.updateFrame.connect(self.movenetWidget.previewThread.updateFrameSlot)

		else:
			self.videoInputWidget = VideoInput.VideoInputWidget(self.centralWidget)
			self.gridLayout.addWidget(self.videoInputWidget, 0, 0, 1, 1)
			self.videoInputWidget.previewThread.updateFrame.connect(self.movenetWidget.previewThread.updateFrameSlot)


		self.switchButton = QPushButton("SWITCH OUTPUT")
		self.gridLayout.addWidget(self.switchButton, 2, 0, 1, 2)
		self.isOutputCamera = True
		self.switchOutputOnClick()

		self.setCentralWidget(self.centralWidget)

		self.retranslateUi(self)

		QMetaObject.connectSlotsByName(self)

	def switchOutputOnClick(self):
		if self.isOutputCamera:
			self.screenWidget.previewThread.updateFrame.disconnect(self.outputWidget.previewThread.updateFrameSlot)
			self.screenWidget.previewThread.updateFrameNP.disconnect(self.outputWidget.previewThread.updateFrameNPSlot)

			if CameraInput:
				self.cameraWidget.previewThread.updateFrame.connect(self.outputWidget.previewThread.updateFrameSlot)
				self.cameraWidget.previewThread.updateFrameNP.connect(self.outputWidget.previewThread.updateFrameNPSlot)
			else:
				self.videoInputWidget.previewThread.updateFrame.connect(self.outputWidget.previewThread.updateFrameSlot)
				self.videoInputWidget.previewThread.updateFrameNP.connect(self.outputWidget.previewThread.updateFrameNPSlot)
		else:
			if CameraInput:
				self.cameraWidget.previewThread.updateFrame.disconnect(self.outputWidget.previewThread.updateFrameSlot)
				self.cameraWidget.previewThread.updateFrameNP.disconnect(self.outputWidget.previewThread.updateFrameNPSlot)
			else:
				self.videoInputWidget.previewThread.updateFrame.disconnect(self.outputWidget.previewThread.updateFrameSlot)
				self.videoInputWidget.previewThread.updateFrameNP.disconnect(self.outputWidget.previewThread.updateFrameNPSlot)

			self.screenWidget.previewThread.updateFrame.connect(self.outputWidget.previewThread.updateFrameSlot)
			self.screenWidget.previewThread.updateFrameNP.connect(self.outputWidget.previewThread.updateFrameNPSlot)

		self.isOutputCamera = not self.isOutputCamera



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
	print("Selected:", app.style().name())
	app.setStyle('windowsvista')

	widget = MainWindow()
	widget.resize(800, 600)
	widget.show()

	if CameraInput:
		app.aboutToQuit.connect(widget.cameraWidget.stopPreviewFeed)
	else:
		app.aboutToQuit.connect(widget.videoInputWidget.stopPreviewFeed)

	app.aboutToQuit.connect(widget.screenWidget.stopPreviewFeed)
	app.aboutToQuit.connect(widget.movenetWidget.stopPreviewFeed)
	app.aboutToQuit.connect(widget.outputWidget.stopPreviewFeed)

	sys.exit(app.exec())
