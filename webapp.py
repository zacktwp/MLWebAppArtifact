from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Iris, User

#import tensorflow as tf
#from keras import backend as K
#from keras.models import load_model
import pandas as pd
import numpy as np
import os
import datetime

import boto3
import io


app = Flask(__name__)


#engine = create_engine('sqlite:///iris.db')
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/ml')
def MLWebApp():
    iris = session.query(Iris).order_by(Iris.created_date.desc()).first()
    return render_template('index.html', iris=iris)

@app.route('/ml/prediction/', methods=['GET', 'POST'])
def prediction():

    if request.method == 'POST':
        newprediction = Iris(
                                sepallength=request.form['sepallength'],
                                sepalwidth=request.form['sepalwidth'],
                                petallength=request.form['petallength'],
                                petalwidth=request.form['petalwidth'])
        session.add(newprediction)
        session.commit()
        return redirect(url_for('results'))
    else:
        return render_template('prediction.html')

@app.route('/ml/results/')
def results():
    iris = session.query(Iris).order_by(Iris.created_date.desc()).first()
    output = [[int(iris.sepallength),
              int(iris.sepalwidth),
              int(iris.petallength),
              int(iris.petalwidth)]]
    #test1 = [[1,1,1,1,1,1,1,1]]
    test = pd.DataFrame(output)

    #prediction localy
    #predictions = ScoringService.predict(test)

    #prediction with sage maker
    payload = test
    #payload_file = io.StringIO()
    payload_file = io.BytesIO()
    payload.to_csv(payload_file, header = None, index = None)

    client = boto3.client('sagemaker-runtime', region_name='us-east-1')
    response = client.invoke_endpoint(EndpointName='sagemaker-decision-trees-2020-03-17-22-26-07-533',
                                      ContentType = 'text/csv',
                                      Body= payload_file.getvalue())
    sagemaker_results = response['Body'].read()
    #return str(predictions), str(sagemaker_results)
    #return str(sagemaker_results)

    return render_template('results.html', sagemaker_prediction=sagemaker_results)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
