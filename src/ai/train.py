import os

import numpy as np
from numpy import newaxis

import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.conv import conv_2d
from tflearn.layers.estimator import regression

import generate_data


def build_model():
	network = input_data(shape=[None, 128, 128, 1], name='input')
	network = conv_2d(network, nb_filter=2, filter_size=5, strides=1, activation='tanh')
	network = fully_connected(network, 1, activation='linear')
	network = regression(network, optimizer='adam', learning_rate=0.001,
						 loss='mean_square', name='target')

	model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='checkpoints/road_model1')
	return model


if __name__ == '__main__':
	input_size = 128
	data_size = 2000

	image_data, label_data = \
		generate_data.generate_batch(
			height=input_size,
			width=input_size,
			minibatch_size=data_size)

	checkpoint_path = 'checkpoints'
	if not os.path.exists(checkpoint_path):
		os.makedirs(checkpoint_path)

	# Train

	X = image_data
	Y = label_data[:,newaxis]

	model = build_model()
	model.fit({'input': X}, {'target': Y}, n_epoch=15,
			   validation_set=0.25,
			   snapshot_step=100, show_metric=True, run_id='road_model1')
