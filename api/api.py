#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stereopickle / Eunjoo Byeon
This script contains Python API
"""

from flask import Flask, request, jsonify
from sklearn.externals import joblib


# defining api
app = Flask(__name__)
app.config["DEBUG"] = True


"""
Multi-label classification of symptoms

There are many ways NF1 can develop and create complications.
Based on descriptions of symptoms, our goal is to provide
possible development so parents can be aware of what to look out for.

Our model will be trained as multi-label classifier on text descriptions
of each possible development. 

Below pipeline will do the following: 
    1. retrieve the text log when '/completelog' is called.
    2. Preprocess text log
    3. Make prediction using multi-label classifier
    4. Return probability of each label
    
"""


@app.route('/classify', methods = ['POST'])
def classify():
    if classifier: 
        try: 
            # run prediction
            return jsonify({ 'class': classes, 
                             'probability': probability })
    else: 
        return ('No Model Found')


if __name__ == '__main__':
    
    try: 
        classifier = model.load('model')
        print ('model successfully loaded')
    except: 
        print ('model failed to load')
    try: 
        c_columns = pickle.load('columns.pkl') 
        print ('columns successfully loaded')
    except: 
        print ('columns failed to load')
        
    app.run()

