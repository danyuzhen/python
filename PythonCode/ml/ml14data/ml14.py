# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tensorflow as tf
from keras.datasets import imdb
import numpy as np
from keras import models
from keras import layers
from keras import losses
from keras import metrics
from keras import optimizers
import matplotlib.pyplot as plt


def vectorize_sequences(sequences, dimension=10000):
    '''
    sequences 是包含所有评论的序列，一条评论对应到一个长度为10000的数组，
    因此我们要构建一个二维矩阵，
    矩阵的行对应于评论数量，列对应于长度为10000
    '''
    results = np.zeros((len(sequences),dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0
    return results




if __name__=='__main__':
    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(path='imdb.npz',num_words=10000)
    word_index=imdb.get_word_index()
    reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
    decoded_review = ' '.join([reverse_word_index.get(i-3, '?') for i in train_data[0]])
    x_train = vectorize_sequences(train_data)
    x_test = vectorize_sequences(test_data)
    y_train = np.asarray(train_labels).astype('float32')
    y_test = np.asarray(test_labels).astype('float32')
    
    model = models.Sequential()
    model.add(layers.Dense(40, activation='sigmoid', input_shape=(10000,)))
    model.add(layers.Dense(20, activation='sigmoid'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizers.RMSprop(lr=0.001), 
                  loss='binary_crossentropy', metrics=['accuracy'])
    x_val = x_train[:10000]
    partial_x_train = x_train[10000:]
    
    y_val = y_train[: 10000]
    partial_y_train = y_train[10000:]
    history = model.fit(partial_x_train, partial_y_train, 
                        epochs=20, batch_size=512, 
                    validation_data = (x_val, y_val))
    
    
    model.fit(x_train, y_train, epochs=4, batch_size=512)
    results = model.evaluate(x_test, y_test)
    print(results)