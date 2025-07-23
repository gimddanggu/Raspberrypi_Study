import cv2
import time

# url = "http://192.168.0.7:81/stream"  # ESP32-CAM 스트림 주소
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라 열기 실패")
    exit()

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    cv2.imshow("Raw Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 전체 평균 FPS 계산
elapsed = time.time() - start_time
fps = frame_count / elapsed
print(f"[📷 ESP32-CAM 평균 FPS] {fps:.2f}")

cap.release()
cv2.destroyAllWindows()