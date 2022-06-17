import os
import pandas as pd
#import db_command.save_feature as save_feature

from tensorflow.keras.models import Model, load_model
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.xception import Xception


def model_definition():
    model = Xception()
    model = Model(inputs=model.inputs, outputs=model.output)
    return model


def img_features(model, img_path):
    img = load_img(img_path, target_size=(299, 299))
    img = img_to_array(img)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    img = preprocess_input(img)
    return model.predict(img)


def save_features(image, category, description, name, price, feature):
    try:
        save_feature(image, category, description, name, price, feature)
    except Exception as e:
        print('Exception : ', e)


def extract_features(data, dataset='Images'):
    model = model_definition()
    for index, item in data.iterrows():
        print(index, ':', item['image'], '=====>>>', item['product_category'])
        path = os.path.join(dataset, item['image'])
        feature = img_features(model, path)
        res = [str(x) for x in feature[0]]
        res = ','.join(res)

        save_features(item['image'], item['product_category'], item['description'], item['product_name'], item['retail_price'], res)


"""def save_feature_model(model):
    model.save('features_extraction_model.h5')


def load_feature_model(model):
    return load_model('features_extraction_model.h5')
"""
#data = pd.read_csv('../static/dataset/dataset_description_csv.csv')
#extract_features(data, '../static/dataset/Images')