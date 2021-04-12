import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import partial
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

path_0 = os.getcwd()

# ---------------------------------------- TRAIN ------------------------------------------

tabla_1 = pd.read_excel(path_0 + '/Data/df_train_0.xlsx', index_col = 'id' )

train_dataset = tabla_1
listado_scores = os.listdir(path_0 + '/Data/scores/')

for lis_ in listado_scores:
    
    df_score = pd.read_excel(path_0 + '/Data/scores/' + lis_, index_col = 0)
    
    if df_score.shape[1] == 2:
        df_score.columns = [lis_[:-5] + '_1', lis_[:-5] + '_2'] 
        train_dataset[[lis_[:-5] + '_1', lis_[:-5] + '_2']] = df_score
        
    else:
        df_score.columns = [lis_[:-5]]
        train_dataset[lis_[:-5]] = df_score

df_y_prima = pd.read_excel(path_0 +'/Data/df_Y_prima_train.xlsx', index_col= 'id')

train_dataset['df_Y_prima'] = df_y_prima
train_labels = train_dataset.pop('df_Y_prima')

X_train = train_dataset
y_train = train_labels

# ---------------------------------------- TEST ------------------------------------------

tabla_1 = pd.read_excel(path_0 + '/Data/df_test_0.xlsx', index_col = 'id' )

train_dataset = tabla_1
listado_scores = os.listdir(path_0 + '/Data/scores_test/')

for lis_ in listado_scores:
    
    df_score = pd.read_excel(path_0 + '/Data/scores_test/' + lis_, index_col = 0)
    
    if df_score.shape[1] == 2:
        df_score.columns = [lis_[:-5] + '_1', lis_[:-5] + '_2'] 
        train_dataset[[lis_[:-5] + '_1', lis_[:-5] + '_2']] = df_score
        
    else:
        df_score.columns = [lis_[:-5]]
        train_dataset[lis_[:-5]] = df_score

df_y_prima = pd.read_excel(path_0 +'/Data/df_Y_prima_test.xlsx', index_col= 'id')

train_dataset['df_Y_prima'] = df_y_prima
train_labels = train_dataset.pop('df_Y_prima')

X_test = train_dataset
y_test = train_labels


'''
X_train, X_test, y_train, y_test = train_test_split( train_dataset, train_labels, test_size=0.2, random_state=42)

w = np.array([[1,2,3,564,5,6,736,8,9,13530], [1,2,3,443,5,643,7,834,9,10]]).astype('float')

ss = StandardScaler()

X_train = ss.fit_transform(w)
X_test = ss.transform(w)
'''

X_train = (X_train - X_train.min()) / (X_train.max() - X_train.min())
X_test = (X_test - X_test.min()) / (X_test.max() - X_test.min())

y_train = (y_train - y_train.min()) / (y_train.max() - y_train.min())
y_test = (y_test - y_test.min()) / (y_test.max() - y_test.min())

X_train.fillna(0, inplace = True)
X_test.fillna(0, inplace = True)

y_train.fillna(0, inplace = True)
y_test.fillna(0, inplace = True)


def create_model():
    # create model
    model = Sequential()
    model.add(layers.Dense(30, input_dim=X_train.shape[1], activation='relu'))
    model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(1))
    # Compile model
    model.compile(optimizer ='adam', loss = tf.keras.losses.MAPE, 
              metrics =[metrics.mae])
    return model

# metrics =[metrics.mae])

model = create_model()

'''

# Define Sequential model with 3 layers
def create_model():
    # create model
    model = Sequential()
    model.add(layers.Dense(5, input_dim=X_train.shape[1], activation='relu'))
    model.add(layers.Dense(2, activation='relu'))
    model.add(layers.Dense(1))
    # Compile model
    model.compile(optimizer ='adam', loss = tf.keras.losses.MAPE, 
              metrics =[metrics.mae])
    return model

model = create_model()
#model.summary()

'''
history = model.fit(X_train, y_train, validation_data=(X_test,y_test), epochs = 100, batch_size=32)

# summarize history for accuracy
plt.plot(history.history['mean_absolute_error'])
plt.plot(history.history['val_mean_absolute_error'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


ress = pd.DataFrame(X_test).copy()
ress['resl_l'] = pd.DataFrame(y_test)
ress['resl_y'] = model.predict(X_test)

ress.to_excel('resssss.xlsx')


