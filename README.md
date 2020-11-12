# NF_Kids_App_PythonAPI
 

## Text Log Classifier Model
There are many different ways NF1 symptoms may develop into further problems.    
We intend to build a NLP model that outputs potential complications based on text log, so the parents and guardians of children can be informed when observing the child with NF1.   

## Prototype
   
For the prototype purpose, we are not training model on the fly. So currently it's calling models directly from the local directory (but scripts to run these are in scripts.py)   

For this prototype purpose, directory structure is as below...   

├── api  
│...├── api.py (contains python api)  
│...└── scripts.py (contains all processing functions)   
├── data   
│...├── keys.csv (in db: symptoms table)   
│...└── symptom_relations.csv (in db: symptoms_relation table)   
└── model   
....├── model.pkl (pickled model)   
....└── symptom_vectors.pkl (pickled average word vectors for symptoms)   

├── 001.EDA.ipynb
├── README.md
├── api
│   ├── __pycache__
│   │   └── scripts.cpython-37.pyc
│   ├── api.py
│   └── scripts.py
├── data
│   ├── NF\ Registry\ NF1\ 092420\ v2.xls
│   ├── keys.csv
│   ├── medical_transcription_samples.csv
│   ├── symptom_relations.csv
│   └── symptoms_existing_data.csv
├── database
│   └── symptoms.db
├── model
│   ├── model.pkl
│   ├── symptom_vectors.pkl
│   ├── word2vec_norm.model
│   └── word2vec_norm.model.vectors.npy
└── target_symptom_vector_keys.pkl
