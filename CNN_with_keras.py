import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import os
from PIL import ImageFile, Image
import numpy as np
from keras.preprocessing import image


url_test = 'C:\\Users\\Osman\\Desktop\\proje\\train_test_Split\\sample\\test'
url_train = 'C:\\Users\\Osman\\Desktop\\proje\\train_test_Split\\sample\\train'
url_prediction = 'C:\\Users\\Osman\\Desktop\\proje\\train_test_Split\\prediction\\bavaria-400-sport-view-390905070fc652b1.jpg'

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
training_set = train_datagen.flow_from_directory(url_train,
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory(url_test,
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'categorical')


cnn = tf.keras.models.Sequential()

cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))

cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

cnn.add(tf.keras.layers.Flatten())

cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))

cnn.add(tf.keras.layers.Dense(units=79, activation='softmax'))

cnn.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# TRAIN
ImageFile.LOAD_TRUNCATED_IMAGES = True
cnn.fit(x = training_set, validation_data = test_set, epochs = 20)


# PREDICTION
test_image = image.load_img(url_prediction_2, target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = cnn.predict(test_image)


result_index = np.where(result == 1.000000e+00)
result_indexOfOne = int(result_index[1][0])
result_indexOfOne

dir_list_dummies = pd.get_dummies(dir_list_train)
dir_list_dummies

np.array(dir_list_dummies[str(dir_list_train[95])],dtype='float')

result_mod = []
result_sub = result[0]
for i in range(len(result_sub)):
    if result_sub[i] == 1:
        result_mod.append(1)
    if result_sub[i] != 1:
        result_mod.append(0)

result_mod = np.array(result_mod)

for i in range(len(dir_list_train)):
    dir_list_dummies_index = np.where(dir_list_dummies[str(dir_list_train[i])] == 1)
    dir_list_dummies_indexOfOne = dir_list_dummies_index[0][0]
    if result_indexOfOne == dir_list_dummies_indexOfOne: 
        print(str(dir_list_train[i]))
    
