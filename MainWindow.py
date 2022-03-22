import sys
from PySide6.QtCore import QSize, QMetaObject, QCoreApplication, QUrl, QFile
from PySide6.QtGui import Qt
from PySide6.QtMultimedia import QMediaDevices, QMediaCaptureSession, QCamera, QMediaPlayer, QImageCapture
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QSizePolicy, QFrame, QApplication, QMainWindow, \
	QTextEdit
from PySide6 import __version__


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(1120, 449)

		self.centralWidget = QWidget(self)
		self.gridLayout = QGridLayout(self.centralWidget)

		self.pushButton = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)

		self.pushButton_2 = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)

		self.label_2 = QLabel(self.centralWidget)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
		self.label_2.setSizePolicy(sizePolicy)
		self.label_2.setMinimumSize(QSize(533, 300))
		self.label_2.setFrameShape(QFrame.Box)
		self.label_2.setFrameShadow(QFrame.Raised)
		self.label_2.setLineWidth(3)
		self.label_2.setAlignment(Qt.AlignCenter)
		self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

		self.label = QLabel(self.centralWidget)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		self.label.setMinimumSize(QSize(533, 300))
		self.label.setFrameShape(QFrame.Box)
		self.label.setFrameShadow(QFrame.Raised)
		self.label.setLineWidth(3)
		self.label.setAlignment(Qt.AlignCenter)
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

		self.log = QTextEdit(self.centralWidget)
		self.gridLayout.addWidget(self.log, 3, 0, 1, 2)

		for dev in QMediaDevices.videoInputs():
			self.log.append("ID: " + dev.id())
			self.log.append("Description: " + dev.description())
			self.log.append("Default: " + str(dev.isDefault()))
			self.log.append("---")
		self.log.append(QMediaDevices.defaultVideoInput().description())

		captureSession = QMediaCaptureSession()
		ig = QImageCapture
		camera = QCamera()
		captureSession.setCamera(camera)
		captureSession.setImageCapture(ig)

		# viewfinder = QVideoWidget()
		# captureSession.setVideoOutput(viewfinder)
		#
		# self.gridLayout.addWidget(viewfinder, 4, 0, 1, 1)
		# viewfinder.show()
		camera.start()
		ig.captureToFile("test.png")

		self.setCentralWidget(self.centralWidget)

		self.retranslateUi(self)

		QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, Window):
		Window.setWindowTitle(QCoreApplication.translate("MainWindow", "OCVSS", None))
		self.pushButton.setText(QCoreApplication.translate("MainWindow", "Choose Camera Input", None))
		self.pushButton_2.setText(QCoreApplication.translate("MainWindow", "Choose Lecture Screen", None))
		self.label_2.setText(QCoreApplication.translate("MainWindow",
		                                                "<html><head/><body><p align=\"center\">LECTURE SCREEN</p></body></html>",
		                                                None))
		self.label.setText(QCoreApplication.translate("MainWindow",
		                                              "<html><head/><body><p align=\"center\">CAMERA INPUT</p></body></html>",
		                                              None))


if __name__ == "__main__":
	print(__version__.__str__())
	app = QApplication([])

	widget = MainWindow()
	widget.resize(800, 600)
	widget.show()

	sys.exit(app.exec())
