from keras.models import Sequential
from keras.optimizers import Adadelta
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.regularizers import l2, activity_l2
import numpy

import os

model = Sequential()

model.add(ZeroPadding2D((1, 1), input_shape=(1, 128, 191)))

model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(6, 4, 4, subsample=(1, 2), W_regularizer=l2(0.01)))
model.add(LeakyReLU())
model.add(Dropout(0.25))

model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(24, 4, 3, subsample=(1, 2), W_regularizer=l2(0.01)))
model.add(LeakyReLU())
model.add(Dropout(0.25))

model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(24, 4, 3, subsample=(2, 2), W_regularizer=l2(0.01)))
model.add(LeakyReLU())
model.add(Dropout(0.25))

model.add(Convolution2D(6, 1, 4, subsample=(1, 2), W_regularizer=l2(0.01)))
model.add(LeakyReLU())
model.add(Dropout(0.25))

model.add(MaxPooling2D(pool_size=(64, 1)))

model.add(Flatten())

model.add(Dense(16))
model.add(LeakyReLU())
model.add(Dropout(0.5))

model.add(Dense(16))
model.add(LeakyReLU())
model.add(Dropout(0.5))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(optimizer=Adadelta(),
              loss='binary_crossentropy')

data = []
labels = []

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for snippet_id in os.listdir('data'):
    dir = 'data/{0}'.format(snippet_id)
    data_tensor = numpy.expand_dims(numpy.load('{0}/spectrogram.npy'.format(dir)), axis=0)
    data.append(data_tensor)
    with open('{0}/class'.format(dir), 'r') as file:
        labels.append(int(file.read()))

data = numpy.stack(data)
labels = numpy.array(labels)

print data.shape
print labels.shape

model.fit(data, labels, nb_epoch=2000, batch_size=32, validation_split=0.2)

print 'Saving model...'
json_string = model.to_json()
open('my_model_architecture.json', 'w').write(json_string)
model.save_weights('my_model_weights.h5', overwrite=True)
