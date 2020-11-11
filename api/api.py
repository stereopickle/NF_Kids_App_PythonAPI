#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stereopickle / Eunjoo Byeon

"""

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from sqlalchemy import create_engine


import joblib
from nlp_model import preprocess



db_connect = create_engine('DATABASE LOCATION')

# defining api
app = Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)

"""
## retrieving necessary data from the database  
For prototype, we need to call ...
1. id, name from symptoms table
2. full symptom_relations table

"""
class Symptoms(Resource):
    def get(self):
        conn = db_connect.connect()
        q = conn.execute("SELECT id, name FROM symptoms;")
        result = {'data': [dict(zip(tuple (q.keys()) ,i)) for i in q.cursor]}
        return jsonify(result)

class Symptoms_Relation(Resource):
    def get(self):
        conn = db_connect.connect()
        q = conn.execute("SELECT * FROM symptoms_relation;")
        result = {'data': [dict(zip(tuple (q.keys()) ,i)) for i in q.cursor]}
        return jsonify(result)


"""
/logresult takes the text, figures out what NF1 related symptoms are present
then return these symptoms and highly correlated potential conditions.

For the prototype, we won't send the extracted symptoms back to database
Instead we will just output the symptom and target condition
to the front-end.
    
"""

@app.route('/logresult', methods = ['POST'])
def logresult():
    text_input = preprocess(text)
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

