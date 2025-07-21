import cv2

url = "http://192.168.0.7:81/stream"

cap = cv2.VideoCapture(url)

while True:
	ret, frame = cap.read()
	if not ret:
		print("Failed to grab frame")
		break;


	# 영상 조작 예시: 흑백 변환
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	cv2.imshow("ESP32-CAM", gray)

	if cv2.waitKey(1) == 27:
		break;	

cap.release();
cv2.destroyAllWindows()
