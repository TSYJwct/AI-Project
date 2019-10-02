#https://www.kaggle.com/deadskull7/best-score-on-kaggle-96-recall
#https://github.com/deadskull7/Pneumonia-Diagnosis-using-XRays-96-percent-Recall/blob/master/Pneumonia%20Diagnosis%20using%20Lung's%20XRay%20.ipynb
#1.데이터 셋 불러오기
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)
train_set = train_datagen.flow_from_directory(
    'chest_xray/train',
    target_size=(64, 64),
    batch_size=25,
    class_mode='categorical'
    )

validation_datagen = ImageDataGenerator(rescale=1./255)
validation_set = validation_datagen.flow_from_directory(
    'chest_xray/val',
    target_size=(64, 64),
    batch_size=5,
    class_mode='categorical'
    )

test_datagen = ImageDataGenerator(rescale=1./255)
test_set = test_datagen.flow_from_directory(
    'chest_xray/test',
    target_size=(64, 64),
    batch_size=15,
    class_mode='categorical'
    )

####################################################
#2.모델구성
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add((Flatten()))
model.add(Dense(128, activation='relu'))
model.add(Dense(2, activation='softmax'))

#######################################################
#3.모델 학습과정 설정
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#######################################################
#4.모델 학습
from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, mode='min',patience=3)
model.fit_generator(
    train_set,
    epochs=20,
    validation_data=validation_set,
    validation_steps=4,
    callbacks=[early_stopping]
)

#########################################################
#5.모델 평가하기
print("--Evaluate--")
scores = model.evaluate_generator(test_set, steps=12)
print("%s: %.2f%%"%(model.metrics_names[1], scores[1] * 100))

###################################################################
#6.모델 사용하기
import numpy as np
print("--Predict--")
output = model.predict_generator(test_set, steps=4)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(test_set.class_indices)
print(output)

#set : 5216 / 16 / 624
#val_acc : 0.5, val_loss : 8.0151 지속, 학습 되지않음
#스탭 4에서 종료된다.
#test Evaluate acc : 61.67