import re
import os
import shutil
import pandas as pd

"""
    This functiion collects the description file of the dataset and reformat it
    to a clear uploadable csv file. It takes 2 parameters:
        - dir-path : path to the directory containing the descriptor file. It's
                    default value is the current directory i.e ''
        - file_name : the name of the descriptor file. This name must be precised

    It then produces a clean data descriptor file named : dataset_descriptor_csv.csv
"""


def data_csv_reformat(file_name, dir_path=''):
    def select_img_present(x):
        exp = '[a-z0-9]*.(jpg|png)'
        if re.match(exp, str(x)):
            return True
        return False

    cols = ['uniq_id', 'crawl_timestamp', 'product_url', 'product_name', 'product_category_tree', 'pid', 'retail_price',
            'discounted_price', 'image', 'is_FK_Advantage_product', 'description', 'product_rating', 'overall_rating',
            'brand', 'product_specifications', 'product_category']
    data = pd.read_csv(dir_path + file_name, delimiter=";", usecols=cols)

    data = data[data['image'].apply(select_img_present)]
    data['product_category'] = data['product_category'].apply(lambda x: x.strip())
    file = dir_path + 'dataset_description_csv.csv'
    data.to_csv(file, index=False)

    return file


"""
    This function helps us segment the dataset (images) into sub-folders according
    to the categorie of the image It takes 3 parameters:
        - data_path : which is the parent directory of the dataset directory
        - df_descriptor : which is the data_frame describing the dataset.
            It can be obtained with the function 'read_data_csv' defined below.
        - data_dir : which is the name of the directory containing the dataset.
                    It's default value is Images
"""


def data_split_into_category(data_path, df_descriptor, data_dir='Images'):
    # Create organised dataset structure
    def create_dir_tree(base_dir=None, categories=[]):
        if base_dir == None:
            base_dir = 'organised'

        try:
            train_dir = os.path.join(base_dir, 'train')
            test_dir = os.path.join(base_dir, 'test')
            os.mkdir(base_dir)
            os.mkdir(train_dir)
            os.mkdir(test_dir)
        except:
            print("Already exists : ", base_dir)

        for cat in categories:
            try:
                os.mkdir(os.path.join(base_dir, 'train', cat))
                os.mkdir(os.path.join(base_dir, 'test', cat))
            except:
                print("Already exists : ", cat)
        return train_dir, test_dir

    base_dir = data_path + '/organised'
    categories = list(df_descriptor['product_category'].unique())
    train_dir, test_dir = create_dir_tree(base_dir, categories=categories)

    data_path += data_dir
    for index, x in df_descriptor.iterrows():
        shutil.copy(os.path.join(data_path, x['image']),
                    os.path.join(base_dir, 'train', x['product_category'], x['image']))

    for cat in categories:
        files = os.listdir(os.path.join(base_dir, 'train', cat))[:15]
        for file in files:
            shutil.move(os.path.join(os.path.join(base_dir, 'train', cat, file)),
                        os.path.join(os.path.join(base_dir, 'test', cat, file)))
    return train_dir, test_dir


"""
    This function helps to open the data description file and return it as a
    pandas dataframe. It have 2 parameters which have been hard-coded for the moment:
        - dir_name : the parent directory of the data description file in csv
        - file_name : the ready processed data description file_name in csv
"""


def read_data_csv(dir_name='../dataset/', file_name='flipkart_com-ecommerce_sample_1050.csv'):
    try:
        file = data_csv_reformat(file_name, dir_name)
        data = pd.read_csv(file)
        return data
    except Exception as e:
        print(e)
        return None


def get_categories():
    return read_data_csv()['product_category'].unique()


"""
    Test function for execution. Not essential !!!
"""


def execute():
    dir_name = '../static/dataset/'
    file_name = 'flipkart_com-ecommerce_sample_1050.csv'

    print('\t*** Descriptor file Reformating\n')
    data_csv_reformat(file_name, dir_path=dir_name)
    data = read_data_csv()

    print('\t*** Dataset spliting into categories')
    images = '../dataset/'
    return data_split_into_category(images, data)

def contextual_preparation():
    dir_name = '../static/dataset/'
    file_name = 'flipkart_com-ecommerce_sample_1050.csv'

    print('\t*** Descriptor file Reformating\n')
    data_csv_reformat(file_name, dir_path=dir_name)
    data = pd.read_csv(dir_name+'dataset_description_csv.csv')

    data_split_into_category(dir_name, data, 'Images')