from flask import Flask, render_template, request
from fastai.vision.all import *
from fastai.vision import *
import pandas as pd
import glob

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def prediction():
    lst1=[]
    confidence_interval=[]
    imagefile=request.files['imagefile']
    image_path = './images/'+imagefile.filename
    imagefile.save(image_path)
    model_1 = load_learner("./models/2_class_guage_model-Retrained.pkl")
    model_2 = load_learner("./models/all_guages-retrained.pkl") #identifier
    prediction_2_class,pred_idx,outputs = model_1.predict(image_path)
    if prediction_2_class=="Gauge":
        pred_class2,pred_idx_,outputs_ = model_2.predict(image_path)
        lst1.append(pred_class2)
        confidence_interval.append(float(outputs_[pred_idx_]*100))
    else:
        lst1.append(prediction_2_class)
        confidence_interval.append(round(float(outputs[pred_idx]*100),2))
    result = str(lst1[0])+ ' ' +str(confidence_interval[0])
    return render_template('index.html',prediction=result)

if __name__=="__main__":
    app.run(port=3000,debug=True)