from flask import Flask


app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

if __name__ == "__main__": # 모든아이피 접속 허용
	app.run(host="0.0.0.0")
