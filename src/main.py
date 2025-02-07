# -*- coding: utf-8 -*-
"""
Title: CNN.

Description: A Convolutional Neural Network.

Created on Sun Jul 10 2022 19:19:01 2022.

@author: Ujjawal .K. Panchal
===

Copyright (c) 2022, Ujjawal Panchal.
All Rights Reserved.
"""
#imports.
import argparse, torch

from torchvision import transforms

import model, pipeline

#static vars.
LR = 1E-3
BS = 128
EPOCHS = 10
DEVICE = "cpu"
NUMCHANNELS = 1
DATASET = "Fashion"
SEED = 42
MODELNAME = "MyCNN"
SAVENAME = f"{DATASET}-{MODELNAME}"

#set torch seed for determinacy.
torch.manual_seed(42)


if __name__ == "__main__":
	#1. load dataset.
	train_set, test_set = pipeline.load_dataset(
									DATASET,
									transform = transforms.Compose([
													transforms.ToTensor(),
													transforms.Normalize(0.1307, 0.3081),
												])
							)
	print(f"Dataset: {type(train_set)=}")
	print(f"Dataset sample: {type(train_set[0][0])=}, {train_set[0][0].size()=}")

	#2. make dataset iterable, shard as batches.
	train_loader = pipeline.get_dataLoader(
						dset = train_set,
						batch_size = BS,
						shuffle = True
					)
	test_loader = pipeline.get_dataLoader(
						dset = test_set,
						batch_size = BS * 2, #Note: this is *2 to speedup testing. test bs doesn't matter.
						shuffle = False
					)

	#2. load our model.
	model = pipeline.make_model(model.CNN, DEVICE, NUMCHANNELS)

	#3. train our model with given iterable shards of batches.
	model = pipeline.train(
					model,
					train_loader,
					EPOCHS,
					LR,
					DEVICE,
			)
	
	#4. test model.
	print("Testing on test set:")
	accuracy, f1, cm = pipeline.test(
							model,
							test_loader,
							DEVICE
						)
	print(f"Accuracy: {accuracy*100:.2f}%\nF1 score: {f1}\nconfusion matrix:\n{cm}")

	#5. save torch model.
	savepath = pipeline.save_model(model, SAVENAME)
	print(f"Saved current model in path: {savepath}")






