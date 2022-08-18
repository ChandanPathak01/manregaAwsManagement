import boto3
from botocore.exceptions import ClientError
s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id = 'AKIAQVWCUMEC62WL74BI',
                        aws_secret_access_key = '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')
path = 'arn:aws:s3:::videotofotos/datasets/'
import os
import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
import matplotlib.pyplot as plt
from tensorflow.keras.layers import BatchNormalization
from keras_preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
#print("hello")
train_dir = path
#test_dir = "C:/Users/adars/Desktop/datasets/face-recognition/AI/datasets/test/"

generator = ImageDataGenerator(rescale=1./255,rotation_range=30,shear_range=0.3,zoom_range=0.3,horizontal_flip=True,fill_mode='nearest')
train_ds = generator.flow_from_directory(train_dir,target_size=(256, 256),batch_size=32)
len(train_ds)

classes =  list(train_ds.class_indices.keys())
print(classes)

model = Sequential()
model.add(Conv2D(32, kernel_size = (3, 3), activation='relu', input_shape=(256,256,3)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(96, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(32, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
#model.add(Dropout(0.3))
model.add(Dense(len(classes),activation='softmax'))
model.compile(
    loss = 'categorical_crossentropy',
    optimizer = 'adam',
    metrics = ["accuracy"])
model.summary()
history = model.fit(train_ds,epochs= 1, batch_size=32)

model = model.save('face_rec_model.h5')






def upload_my_file(bucket, folder, file_to_upload, file_name):

    key = folder+"/"+file_name
    try:
        response = s3_client.upload_file(file_to_upload, bucket, key, ExtraArgs={'ACL':'public-read'})
        file_url = '%s/%s/%s' % (s3_client.meta.endpoint_url, bucket, key)
        
    except ClientError as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False
    return True


#Upload file
upload_my_file("videotofotos", "trainedModel", str(model), 'trainedModel.h5' )