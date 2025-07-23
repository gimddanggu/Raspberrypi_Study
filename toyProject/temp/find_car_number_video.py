# 필요한 라이브러리
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pytesseract
from PIL import Image
import paho.mqtt.client as mqtt
import re
import time
car_number = ""
mqtt_broker_ip = "192.168.0.6"
port = 1883
topic = "car/number"
username = "dahyun_raspi"
password = "0101"  # 설정한 비밀번호

last_plate = None
last_time = 0
cooldown = 10 # 10초 이내 같은 번호판이 인식되었을 경우 무시

# MQTT 초기 설정 
pattern = r'^\d{3}[가-힣]\d{4}$'
client = mqtt.Client()
client.username_pw_set(username=username, password=password)
client.connect(mqtt_broker_ip, port, 60)
client.loop_start()

# contours box 저장 함수
def draw_contours(contours):
    contours_dict = []
    # 검출된 영역 저장
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contours_dict.append({
            'contour':contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (h / 2), # 가로 길이
            'cy': y + (h / 2), # 세로 길이
        })
    print(f"[DEBUG]검출된 영역 저장: {len(contours_dict)}개")    
    return contours_dict

# Contours 에서 번호판 영역 찾기 -----------
def find_possible_contours(contours_dict):
    MIN_AREA, MIN_WIDTH, MIN_HEIGHT = 80, 2, 8
    MIN_RATIO, MAX_RATIO = 0.25, 1.0

    possible_contours = []
    cnt = 0
    for c in contours_dict:
        area = c['w'] * c['h']
        ratio = c['w'] / c['h']

        if area > MIN_AREA and c['w'] > MIN_WIDTH and c['h'] > MIN_HEIGHT and MIN_RATIO < ratio < MAX_RATIO:
            c['idx'] = cnt
            cnt += 1
            possible_contours.append(c)

    print(f"[DEBUG]영역 크기로 필터링된 contours: {len(possible_contours)}개")    
    return possible_contours

def find_chars(contour_list):
    MAX_DIAG_MULTIPLYER = 4
    MAX_ANGLE_DIFF = 12.0
    MAX_AREA_DIFF = 0.4
    MAX_WIDTH_DIFF = 0.6
    MAX_HEIGHT_DIFF = 0.2
    MIN_N_MATCHED = 4

    matched_result_idx = []

    for c1  in contour_list:
        matched_contours_idx = []
        for c2 in contour_list:
            if c1['idx'] == c2['idx']: # 같은 contour 비교시 continue
                continue;

            dx = abs(c1['cx'] - c2['cx'])
            dy = abs(c1['cy'] - c2['cy'])

            diagonal_length = np.sqrt(c1['w'] ** 2 + c1['h'] ** 2)

            distance = np.linalg.norm(np.array([c1['cx'], c1['cy']]) - np.array([c2['cx'], c2['cy']]))
            if dx == 0:
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dy / dx))
            area_diff = abs(c1['w'] * c1['h'] - c2['w'] * c2['h']) / (c1['w'] * c1['h'])
            width_diff = abs(c1['w'] - c2['w']) / c1['w']
            height_diff = abs(c1['h'] - c2['h']) / c1['h']
        
            if distance < diagonal_length * MAX_DIAG_MULTIPLYER \
            and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
            and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                matched_contours_idx.append(c2['idx'])
                
        matched_contours_idx.append(c1['idx'])
        
        if len(matched_contours_idx) < MIN_N_MATCHED:
            continue
            
        matched_result_idx.append(matched_contours_idx)
        
        unmatched_contour_idx = []
        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
                unmatched_contour_idx.append(d4['idx'])
        
        unmatched_contour = np.take(possible_contours, unmatched_contour_idx)
        
        recursive_contour_list = find_chars(unmatched_contour)
        
        for idx in recursive_contour_list:
            matched_result_idx.append(idx)
            
        break
        
    return matched_result_idx

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)  # 창 크기 조절 가능하게 설정
cv2.resizeWindow("Frame", 600, 480)         # 원하는 해상도로 창 크기 설정
cap = cv2.VideoCapture("http://192.168.0.7:81/stream")
# cap =  cv2.VideoCapture(0)
frame_count = 0
while True:
    start_time = time.time()
    frame_count += 1
    if frame_count % 5 != 0:
        continue
    ret, frame = cap.read()
    if not ret:
        break
    if ret:
        # 흑백 이미지로 변환
        blur_frame = cv2.GaussianBlur(frame, (5, 5), sigmaX=0)
        gray_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2GRAY)

        # Thresholding
        _, thresh_blur_frame = cv2.threshold(gray_frame, 215, 255, cv2.THRESH_BINARY)
        # 윤곽선 찾기
        contours_blur, _ = cv2.findContours(thresh_blur_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        temp_result_blur = np.zeros(frame.shape, dtype=np.uint8)
        # 윤곽선 그리기
        cv2.drawContours(temp_result_blur, contours_blur, contourIdx=-1, color=(255,255,255))
        cv2.imshow("t", temp_result_blur)
        contours_dict = draw_contours(contours_blur) 
        possible_contours = find_possible_contours(contours_dict)
        temp_result_blur = np.zeros(frame.shape, dtype=np.uint8)

        result_idx = find_chars(possible_contours)
        matched_result = []
        for idx_list in result_idx:
            matched_result.append(np.take(possible_contours, idx_list))
        plate_region = np.zeros(frame.shape, dtype=np.uint8)
        for group in matched_result:
            x_min = min([d['x'] for d in group])
            y_min = min([d['y'] for d in group])
            x_max = max([d['x'] + d['w'] for d in group])
            y_max = max([d['y'] + d['h'] for d in group])

            # 번호판 전체 박스 그리기
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            plate_region = frame[y_min:y_max, x_min:x_max]
        cv2.imshow("Frame", frame)
        flipped = cv2.flip(plate_region, 1)
        cv2.imshow("plate_region", flipped)


        # # ocr을 위한 번호판 확대 이미지
        gray = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # 확대
        blur = cv2.GaussianBlur(gray, (3, 3), 0)  # 노이즈 제거
        _, thresh = cv2.threshold(blur, 121, 255, cv2.THRESH_BINARY)  # 이진화

        # OCR
        pytesseract.pytesseract.tesseract_cmd = r"C:\Dev\Tool\Tesseract-OCR\tesseract.exe"
        chars = pytesseract.image_to_string(thresh, lang='kor', config='--psm 7 --oem 0')
        print(f"[DEBUG]📄 추출된 텍스트: {chars.strip()}")
        plate_number = chars.strip()
        if not plate_number:
            continue
        # cv2.imshow(plate_region, cmap='gray')s
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break



    # mqtt 전송
    ## 번호판 형식 000가000 이면 전송
        
    # 번호판 정보 보냄
    if plate_number and re.match(pattern, plate_number):
        now = time.time()
        if plate_number != last_plate or (now - last_time) > cooldown:
            result = client.publish(topic, plate_number)
            result.wait_for_publish()

            # 전송 완료 확인 
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                last_plate = plate_number
                print("번호판 전송 완료")
            else:
                print(f"번호판 전송 실패, 코드: {result.rc}")
        else:
            print(f"[DEBUG] 이미 처리된 번호판입니다.")
    else:
        print("[DEBUG] 번호판 형식이 아닙니다")

# 종료 시
cap.release()
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()