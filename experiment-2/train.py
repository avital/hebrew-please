from keras.models import Sequential
from keras.optimizers import Adadelta
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D
import numpy

import os

model = Sequential()
model.add(Convolution2D(5, 7, 3, subsample=(2, 2), activation='tanh', input_shape=(1, 128, 95)))
model.add(MaxPooling2D(pool_size=(7, 4)))
model.add(Flatten())
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

model.fit(data, labels, nb_epoch=5000, batch_size=32, validation_split=0.2)

print 'Saving model...'
json_string = model.to_json()
open('my_model_architecture.json', 'w').write(json_string)
model.save_weights('my_model_weights.h5', overwrite=True)
