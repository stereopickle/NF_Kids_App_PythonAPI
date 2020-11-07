import flask as fl

app = fl.Flask(__name__)
app.config["DEBUG"] = True

# test data 

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
