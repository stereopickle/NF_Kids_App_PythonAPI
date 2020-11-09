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
of each possible development. (need to collect data)

Below pipeline will do the following: 
    1. retrieve the text log when '/completelog' is called.
    2. Preprocess text log
    3. Make prediction using multi-label classifier
    4. Return probability of each label
    
"""




dat = [
       {'id': 0, 
	'prop1': 'test', 
	'prop2': 'test2', 
	'prop3': 'test3'
	},
	{'id': 1, 
	'prop1': 'test1-1', 
	'prop2': 'test1-2', 
	'prop3': 'test1-3'
	},
	{'id': 2,
	'prop1': 'test2-1',
	'prop2': 'test2-2', 
	'prop3': 'test2-3'
	}
]

@app.route('/', methods = ['GET'])

def home():
	return '<p>Test Homepage</p>'

# return 
@app.route('/api/v1/resources/data/test', methods = ['GET'])

def api_test():
       return fl.jsonify(dat)

app.run()
