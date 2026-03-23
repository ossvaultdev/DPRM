import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

import os 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import (
    Conv2D,
    MaxPooling2D,
    Activation,
    Dropout,
    Flatten,
    Dense,
    Input,
)
from keras.utils import to_categorical

(X_train, y_train), (X_val, y_val) = cifar10.load_data()
X_train = X_train / 255.0
X_val = X_val / 255.0

y_train = to_categorical(y_train, 10)
y_val = to_categorical(y_val, 10)

model = Sequential(
    [
        Conv2D(32, (3, 3), padding="same", input_shape=X_train.shape[1:]),
        Activation("relu"),
        Conv2D(32, (3, 3)),
        Activation("relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(512),
        Activation("relu"),
        Dropout(0.5),
        Dense(10),
        Activation("softmax"),
    ]
)

print("model.compile::...............................................................................")
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
print("model.fit::...............................................................................")
model.fit(X_train, y_train, batch_size=64, epochs=10, validation_data=(X_val, y_val))
print("model.evaluate:...............................................................................")
score = model.evaluate(X_val, y_val, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

model.save("cifar10_model_2.h5")
