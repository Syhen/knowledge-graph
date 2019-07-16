# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/27 上午10:30
"""
import tensorflow as tf
import numpy as np
inputs = tf.keras.layers.Input((128, ))
x = tf.keras.layers.Dense(64, activation="relu")(inputs)
x = tf.keras.layers.Dense(1, activation="sigmoid")(x)
model = tf.keras.models.Model(inputs, x)
model.compile("adam", "binary_crossentropy")
output = model(np.random.rand(64, 128))
print("finished")
