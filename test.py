# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:26:00 2019

@author: isstjh
"""

import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt


from tensorflow.keras.callbacks import ModelCheckpoint,CSVLogger,LearningRateScheduler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import add
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import cifar10
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential



plt.style.use('ggplot')     # if want to use the default style, set 'classic'
plt.rcParams['ytick.right']     = True
plt.rcParams['ytick.labelright']= True
plt.rcParams['ytick.left']      = False
plt.rcParams['ytick.labelleft'] = False
plt.rcParams['font.family']     = 'Arial'


# .............................................................................
datagen = ImageDataGenerator(validation_split=0.2)
train_it = datagen.flow_from_directory('data/train/', shuffle=True, target_size=(32,32), class_mode='categorical', batch_size=8, subset='training')
# load and iterate validation dataset
val_it = datagen.flow_from_directory('data/train/', shuffle=True, target_size=(32,32), class_mode='categorical', batch_size=8, subset='validation')
# load and iterate test dataset
#test_it = datagen.flow_from_directory('data/test/', target_size=(256,256), class_mode='categorical', batch_size=8, subset)

seed = 7
np.random.seed(seed)
modelname = 'ca2'
#optmz       = optimizers.Adam(lr=0.05, decay = 0.0001)

filepath        = modelname + ".hdf5"
checkpoint      = ModelCheckpoint(filepath, 
                                  monitor='val_acc', 
                                  verbose=0, 
                                  save_best_only=True, 
                                  mode='max')

                            # Log the epoch detail into csv
csv_logger      = CSVLogger(modelname +'.csv')
callbacks_list  = [checkpoint,csv_logger]
def createModel():
    inputs = Input(shape=(32,32,3))
    y = Conv2D(256, 3, padding='same', activation='relu')(inputs)
    y = MaxPooling2D(pool_size=(2,2))(y)
    y = Conv2D(384, 3, padding='same', activation='relu')(y)
    y = MaxPooling2D(pool_size=(2,2))(y)
    y = Conv2D(512, 3, padding='same', activation='relu')(y)
    y = MaxPooling2D(pool_size=(2,2))(y)
    y = Flatten()(y)
    y = Dense(1024, activation='relu')(y)
    y = Dense(512, activation='relu')(y)
    y = Dense(256, activation='relu')(y)
    y = Dense(128, activation='relu')(y)
    y = Dense(64, activation='relu')(y)
    y = Dense(32, activation='relu')(y)
    y = Dense(3, activation='softmax')(y)
    model = Model(inputs=inputs, outputs=y)
    model.compile(loss='kullback_leibler_divergence', optimizer='adam', metrics=['accuracy'])
    return model

# define model
model = createModel()
model.summary()
# fit model
model.fit_generator(train_it, validation_data=val_it,epochs=200,callbacks=callbacks_list)

# .............................................................................

