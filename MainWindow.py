import sys

from PySide2.QtCore import QMetaObject, QCoreApplication
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QMainWindow
from PySide2 import __version__

import Camera
import Screen


class MainWindow(QMainWindow):

	def showCam(self):
		print("Active state:", self.camera.status())

	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(1120, 449)

		self.centralWidget = QWidget(self)
		self.gridLayout = QGridLayout(self.centralWidget)


		self.pushButton = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)

		self.pushButton_2 = QPushButton(self.centralWidget)
		self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)


		# self.log = QTextEdit(self.centralWidget)
		# self.gridLayout.addWidget(self.log, 3, 0, 1, 2)

		# TEST AREA START

		# for dev in QCameraInfo.availableCameras():
		# 	print(dev.description())

		self.cameraWidget = Camera.CameraWidget(self.centralWidget)
		self.gridLayout.addWidget(self.cameraWidget, 0, 0, 1, 1)

		self.screenWidget = Screen.ScreenWidget(self.centralWidget)
		self.gridLayout.addWidget(self.screenWidget, 0, 1, 1, 1)

		# TEST AREA END

		self.setCentralWidget(self.centralWidget)

		# self.retranslateUi(self)

		QMetaObject.connectSlotsByName(self)



	def retranslateUi(self, Window):
		Window.setWindowTitle(QCoreApplication.translate("MainWindow", "OCVSS", None))
		self.pushButton.setText(QCoreApplication.translate("MainWindow", "Choose Camera Input", None))
		self.pushButton_2.setText(QCoreApplication.translate("MainWindow", "Choose Lecture Screen", None))
		self.label_2.setText(QCoreApplication.translate("MainWindow",
		                                                "<html><head/><body><p align=\"center\">LECTURE SCREEN</p></body></html>",
		                                                None))





if __name__ == "__main__":
	print("Qt version:", __version__.__str__())
	app = QApplication(sys.argv)

	widget = MainWindow()
	widget.resize(800, 600)
	widget.show()

	sys.exit(app.exec_())
