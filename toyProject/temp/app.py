from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
from datetime import datetime
import cv2
app = Flask(__name__)
import video_processor  # 영상 처리 모듈 (임시 이름)

app.secret_key = "dev_key"

# cap = cv2.VideoCapture("http://192.168.0.7:81/stream")  # app.py에서 정의

# 관리자 계정
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

def gennerate_main():
		while True:
			frame = video_processor.process_frame()
			if frame is None:
				continue
		
			ret, buffer =  cv2.imencode('.jpg', frame)
			frame_bytes = buffer.tobytes()

			yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
			
def gennerate_plate():
	while True:
		plate = video_processor.get_plate_region()
		if plate is None:
			continue

		ret, buffer = cv2.imencode('.jpg', plate)
		plate_bytes = buffer.tobytes()

		yield (b'--frame\r\n'
		 	   b'Content-Type: image/jepg\r\n\r\n' + plate_bytes + b'\r\n')


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

@app.route('/video_feed')
def video_feed():
	print("[video_feed 호출됨]") 
		
	return Response(gennerate_main(),
				mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/plate_feed')
def plate_feed():
	return Response(gennerate_plate(),
				 mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/plate_text')
def get_plate_text():
	plate_text = video_processor.OCR()
	return jsonify({
        "plate_text": plate_text if plate_text else "인식 실패1",
        "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def update_plate_result(img, text):
#     global plate_text
#     plate_text = text
#     cv2.imwrite(plate_image_path, img)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5088)
