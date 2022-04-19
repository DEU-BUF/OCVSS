import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_docs.vis import embed
import numpy as np
import cv2
from subprocess import run, PIPE

from matplotlib import pyplot as plt
import matplotlib.patches as patches

import imageio
from IPython.display import HTML, display

from TensorHelper import *


def main():
	model_name = "movenet_lightning_int8 tflite"
	download_command = ["wget", "-q", "-nc", "-O", "model.tflite"]
	if "tflite" in model_name:
		out = ""
		if "movenet_lightning_f16" in model_name:
			out = run(download_command + ["https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/float16/4?lite-format=tflite"], stdout=PIPE)
			input_size = 192
		elif "movenet_thunder_f16" in model_name:
			out = run(download_command + ["https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/float16/4?lite-format=tflite"], stdout=PIPE)
			input_size = 256
		elif "movenet_lightning_int8" in model_name:
			out = run(download_command + ["https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/int8/4?lite-format=tflite"], stdout=PIPE)
			input_size = 192
		elif "movenet_thunder_int8" in model_name:
			out = run(download_command + ["https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/int8/4?lite-format=tflite"], stdout=PIPE)
			input_size = 256
		else:
			raise ValueError("Unsupported model name: %s" % model_name)
		print(out.stdout.decode("UTF-8"))
		print(out.returncode)

		# Initialize the TFLite interpreter
		interpreter = tf.lite.Interpreter(model_path="model.tflite")
		interpreter.allocate_tensors()

		def movenet(input_image):
			"""Runs detection on an input image.

			Args:
			  input_image: A [1, height, width, 3] tensor represents the input image
				pixels. Note that the height/width should already be resized and match the
				expected input resolution of the model before passing into this function.

			Returns:
			  A [1, 1, 17, 3] float numpy array representing the predicted keypoint
			  coordinates and scores.
			"""
			# TF Lite format expects tensor type of uint8.
			input_image = tf.cast(input_image, dtype=tf.uint8)
			input_details = interpreter.get_input_details()
			output_details = interpreter.get_output_details()
			interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
			# Invoke inference.
			interpreter.invoke()
			# Get the model prediction.
			keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
			return keypoints_with_scores

	else:
		if "movenet_lightning" in model_name:
			module = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
			input_size = 192
		elif "movenet_thunder" in model_name:
			module = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
			input_size = 256
		else:
			raise ValueError("Unsupported model name: %s" % model_name)

		def movenet(input_image):
			"""Runs detection on an input image.

			Args:
			  input_image: A [1, height, width, 3] tensor represents the input image
				pixels. Note that the height/width should already be resized and match the
				expected input resolution of the model before passing into this function.

			Returns:
			  A [1, 1, 17, 3] float numpy array representing the predicted keypoint
			  coordinates and scores.
			"""
			model = module.signatures['serving_default']

			# SavedModel format expects tensor type of int32.
			input_image = tf.cast(input_image, dtype=tf.int32)
			# Run model inference.
			outputs = model(input_image)
			# Output is a [1, 1, 17, 3] tensor.
			keypoints_with_scores = outputs['output_0'].numpy()
			return keypoints_with_scores

	out = run(["curl", "-o", "input_image.jpeg", "https://images.pexels.com/photos/4384679/pexels-photo-4384679.jpeg", "--silent"], stdout=PIPE)
	print(out.stdout.decode("UTF-8"))
	print(out.returncode)

	# Load the input image.
	image_path = 'input_image.jpeg'
	image = tf.io.read_file(image_path)
	image = tf.image.decode_jpeg(image)

	# Resize and pad the image to keep the aspect ratio and fit the expected size.
	input_image = tf.expand_dims(image, axis=0)
	input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

	# Run model inference.
	keypoints_with_scores = movenet(input_image)

	# Visualize the predictions with image.
	display_image = tf.expand_dims(image, axis=0)
	display_image = tf.cast(tf.image.resize_with_pad(
		display_image, 1280, 1280), dtype=tf.int32)
	output_overlay = draw_prediction_on_image(
		np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

	plt.figure(figsize=(5, 5))
	plt.imshow(output_overlay)
	plt.imsave("output_image.jpeg", output_overlay)
	_ = plt.axis('off')





if __name__ == "__main__":
	main()
