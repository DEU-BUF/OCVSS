import sys
from cv2 import VideoCapture, flip, setLogLevel, VideoWriter_fourcc, cvtColor
from cv2 import CAP_V4L2, CAP_DSHOW, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FOURCC, CAP_PROP_BACKEND, COLOR_BGR2RGB
from numpy import ndarray, array as np_array
from PySide6.QtMultimedia import QMediaDevices, QVideoFrameFormat
from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, Qt, QPixmap

import tensorflow as tf
from TensorHelper import *

import Preview

import cv2

class MovenetWidget(Preview.PreviewWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.previewThread.movenettenFrameGeldi.connect(self.updateFrameSlot)
		self.changeBtn.hide()

	def updateFrameSlot(self, image):
		#TODO
		self.previewView.setPixmap(QPixmap.fromImage(image.copy(0, 75, 347, 196).scaled(640, 360)))

	class Thread(Preview.PreviewWidget.Thread):
		movenettenFrameGeldi = Signal(QImage)
		inputIndex = 0
		movenet_frame = -1
		# tf
		input_size = 192

		def __init__(self, parent, previewSize, outputCamera):
			super().__init__(parent, previewSize)
			self.previewSize = previewSize
			self.interpreter = tf.lite.Interpreter(model_path="model.tflite")
			self.interpreter.allocate_tensors()

		def run(self):
			self.ThreadActive = True

		#def updateFrameSlot(self, frame): #real name is this
		def movenetFrameIsleSlot(self, frame):
			self.movenet_frame = (self.movenet_frame + 1) % 30
			if self.movenet_frame == 0:
				# TODO PROCESS IS HERE
				input_frame = tf.expand_dims(frame, axis=0)
				input_frame = tf.image.resize_with_pad(input_frame, self.input_size, self.input_size)

				keypoints_with_scores = self.movenet(input_frame, self.interpreter)

				display_image = tf.expand_dims(frame, axis=0)
				#TODO make this 720 to make borders cease to exist
				display_image = tf.cast(tf.image.resize_with_pad(display_image, 1280, 1280), dtype=tf.int32)
				output_overlay = draw_prediction_on_image(np.squeeze(display_image.numpy(), axis=0),
				                                          keypoints_with_scores)

				colorCorrectedFrame = cvtColor(np_array(output_overlay), COLOR_BGR2RGB)

				colorCorrectedFrame = flip(colorCorrectedFrame, 1)

				frameInQtFormat = QImage(colorCorrectedFrame.data, colorCorrectedFrame.shape[1],
				                         colorCorrectedFrame.shape[0],
				                         QImage.Format_RGB888)
				finalFrame = frameInQtFormat.scaled(self.previewSize.width(), self.previewSize.height(),
				                                    Qt.KeepAspectRatio)

				finalFrame = finalFrame.copy(3, 4, 347, 347)  # cropping white borders

				# self.updateFrame.emit(frame) #real frame sending signal will be this
				self.movenettenFrameGeldi.emit(finalFrame)

		def movenet(self, input_image, interpreter):
			# TF Lite format expects tensor type of uint8.
			input_image = tf.cast(input_image, dtype=tf.uint8)
			input_details = interpreter.get_input_details()
			output_details = interpreter.get_output_details()
			interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
			# Invoke inference.
			interpreter.invoke()
			# Get the model prediction.
			keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
			# f = open("keypoints.txt", "w")
			# f.write(str(input_details[0]))
			# f.write("\n")
			# f.write(str(output_details[0]))
			# f.close()
			return keypoints_with_scores

