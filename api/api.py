#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stereopickle / Eunjoo Byeon

"""

from flask import Flask, request, jsonify
import joblib
from nlp_model import preprocess

# defining api
app = Flask(__name__)
app.config["DEBUG"] = True


"""
/logresult takes the text, figures out what NF1 related symptoms are present
then return these symptoms and highly correlated potential conditions.

For the prototype, we won't send the extracted symptoms back to database
Instead we will just output the symptom and target condition
to the front-end.
    
"""

@app.route('/logresult', methods = ['POST'])
def logresult():
    if classifier: 
        try: 
            # run nlp
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

