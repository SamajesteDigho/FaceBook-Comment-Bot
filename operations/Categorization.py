import os
import numpy as np

from tensorflow.keras.applications.xception import Xception
from keras.models import Model, load_model
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.xception import preprocess_input

from .Data_Preparation import get_categories

data_path = 'organised_dataset'

train_dir = os.path.join(data_path, 'train')
test_dir = os.path.join(data_path, 'test')


def model_definition(nb_classes):
    model = Xception()
    # model = Model(inputs=model.inputs, outputs=model.outputs)
    model.trainable = False
    x = Dense(512, activation='relu')(model.output)
    y = Dense(nb_classes, activation='softmax')(x)
    model = Model(inputs=model.input, outputs=y)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


def data_upload(train_dir, test_dir):
    train_dg = ImageDataGenerator(rescale=1. / 255,
                                  shear_range=0.2,
                                  zoom_range=0.2,
                                  horizontal_flip=True)
    test_dg = ImageDataGenerator(rescale=1. / 255,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)

    train_set = train_dg.flow_from_directory(train_dir,
                                             target_size=(299, 299),
                                             batch_size=32,
                                             class_mode='categorical')
    test_set = test_dg.flow_from_directory(test_dir,
                                           target_size=(229, 229),
                                           batch_size=32,
                                           class_mode='categorical')

    return train_set, test_set


def save_trained_model(model, name='categorizeModel'):
    model.save(''.join([name, '.h5']))


def load_trained_model():
    return load_model('models/categorizeModel.h5')


def training_model(model, train_set, test_set, epoch=5):
    model.fit(train_set, epochs=epoch, validation_data=test_set)
    save_trained_model(model)

    # Printing Obtained Results
    print('=============================================')
    print('=============================================')
    valid_loss, valid_accuracy = model.evaluate(test_set)
    print('Accuracy Obtained : {}%'.format(round(valid_accuracy, 2)))
    print('=============================================')


def categorise_process():
    print('====================================')
    print('\t PROCESS STARTED !!! ')
    print('====================================')

    # Prepare and essure data is cleared
    print('*** Preparing the dataset\n')
    train_dir, test_dir = dp.execute()

    # Upload data from different dirs
    print('-------------------------------------')
    print('Uploading dataset into train and test sets\n')
    train_set, test_set = data_upload(train_dir, test_dir)

    # Get the number of categories present
    print('-------------------------------------')
    print('Get the number of categories\n')
    nb_class = len(dp.get_categories())

    # Define the model
    print('-------------------------------------')
    print('Defining the training model\n')
    model = model_definition(nb_class)

    # Trainand save the model
    print('-------------------------------------')
    print('Training the model\n')
    training_model(model, train_set, test_set)

    print('\n Model trained and saved\n')


def predict_category(model, img_path):
    img_ = load_img(img_path, target_size=(299, 299))  # Xception input size
    img_ = img_to_array(img_)
    img_ = img_.reshape((1, img_.shape[0], img_.shape[1], img_.shape[2]))
    img_ = preprocess_input(img_)  # preprocess image as CNN model want (normalize pixel value to (-1,1))
    y = model.predict(img_)

    #categories = get_categories()
    categories = ['Baby Care', 'Beauty and Personal Care', 'Computers', 'Home Decor & Festive Needs', 'Home Furnishing', 'Kitchen & Dining', 'Watches']

    return categories[np.argmax(y[0])]