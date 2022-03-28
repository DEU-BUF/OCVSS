import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_docs.vis import embed
import numpy as np
import cv2

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches

import imageio


def main():
	model_name = "movenet_lightning"

	# if "tflite" in model_name:
	# 	if "movenet_lightning_f16" in model_name:
	# 		!wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/float16/4?lite-format=tflite
	# 		input_size = 192
	# 	elif "movenet_thunder_f16" in model_name:
	# 		!wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/float16/4?lite-format=tflite
	# 		input_size = 256
	# 	elif "movenet_lightning_int8" in model_name:
	# 		!wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/int8/4?lite-format=tflite
	# 		input_size = 192
	# 	elif "movenet_thunder_int8" in model_name:
	# 		!wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/int8/4?lite-format=tflite
	# 		input_size = 256
	# 	else:
	# 		raise ValueError("Unsupported model name: %s" % model_name)







if __name__ == "__main__":
	main()
