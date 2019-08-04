#!/usr/bin/python
from keras.models import Sequential, Model
from keras.layers import Dense
from keras.optimizers import Adam
from preprocessing import *

data = readready()

X_train, train_labels = get_prepare_data(data)

model = Sequential([
    Dense(64, activation='sigmoid', input_shape=(X_train.shape[1],)),
    Dense(128, activation='sigmoid'),
    Dense(1, activation='sigmoid')
])

# Set Optimizer
opt = Adam(lr=0.00001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(X_train, train_labels, batch_size=32, shuffle=True, epochs=15)

