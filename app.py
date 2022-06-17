import operations.Categorization as CT
import operations.db_command as db
import operations.Feature_Extraction as FE
import operations.Governor as GVN

import os



from flask import Flask, render_template, request, redirect

app = Flask('')
app.config['SECRET_KEY'] = 'samajesteDigho'
app.config['UPLOAD_FOLDER'] = Images = os.path.join('static', 'dataset','Images')

"""
    Models upload
"""
model1 = CT.load_trained_model()
model2 = FE.model_definition()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/predict', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST' and 'image' in request.files:
        img = request.files['image']
        # Save image file
        img_path = 'static/Images/received_image.'+img.filename.split('.')[-1]
        img.save(img_path)

        # Processing image process
        category = CT.predict_category(model1, img_path)
        cat_feat = db.get_features_category('models/features.db', category) #.rowcount
        ref = FE.img_features(model2, img_path)
        ref = [x for x in ref[0]]
        distances = GVN.calculate_distance_and_sort(ref, cat_feat)[:15]

        selected = [{'img':os.path.join('static/dataset/Images', x[0]['image']), 'object':x[0]} for x in distances]

        return render_template('result.html', category=category, source=img_path, img_set=selected)
    else:
        return render_template('result.html')