from flask import Flask, request

app = Flask(__name__)

@app.route('/')

def helloWorld():
	return "hello World"

@app.route('/name')
def name():
	return "<h1>my name is Kim dahyun</h1>"
@app.route('/address')
def address():
	return "<h2>my house's address is Ulsan</h2>"
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)	
