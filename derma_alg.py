# -*- coding: utf-8 -*-
"""Copy of THE DERMA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U6p7HrmtG0_5-OPxInXkUki6Js0C4G4e
"""

import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import h5py

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from keras import layers, models
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from sys import getsizeof

img_width = 128
img_height = 128
batch_size = 128

train_images = tf.keras.preprocessing.image_dataset_from_directory(
    '/content/drive/MyDrive/DERMNET/Train/',
    labels='inferred',
    label_mode = "categorical", 
    color_mode='rgb',
    batch_size= batch_size,
    image_size=(img_height,img_width),
    shuffle=True,
    seed=123,
)

test_images = tf.keras.preprocessing.image_dataset_from_directory(
    '/content/drive/MyDrive/DERMNET/Test/',
    labels="inferred",
    label_mode = "categorical", 
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height,img_width),
    shuffle=True,
    seed=123,
)

data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)

model = models.Sequential()
model.add(keras.Input(shape = (128,128, 3)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(3))

data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(
    train_images, 
    epochs = 10, 
    batch_size = 128, 
    validation_data = test_images
    )

KERAS_MODEL_NAME = "derma_alg.h5"

model.save(KERAS_MODEL_NAME)

TF_LITE_MODEL_FILE_NAME = "tf_lite_derma_alg.tflite"

tf_lite_converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = tf_lite_converter.convert()

tflite_model_name = TF_LITE_MODEL_FILE_NAME
open(tflite_model_name, "wb").write(tflite_model)