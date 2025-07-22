from flask import Flask, render_template, request, redirect, url_for, session, Response
from datetime import datetime
app = Flask(__name__)
app.secret_key = "dev_key"

# 관리자 계정
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

@app.route('/')
def home():
	return redirect(url_for("login"))

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
			session['logged_in'] = True
			return redirect(url_for('monitor'))
		else:
			return render_template("login.html", error="아이디 또는 비밀번호가 틀렸습니다.")

	return render_template("login.html")


@app.route('/stream')
def stream():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	return render_template("stream.html")

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('login'))

@app.route('/monitor')
def monitor():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template(
        'index.html',
        plate_text="test",
        now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def update_plate_result(img, text):
#     global plate_text
#     plate_text = text
#     cv2.imwrite(plate_image_path, img)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
