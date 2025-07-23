import cv2
import numpy as np
import pytesseract
from PIL import Image
import paho.mqtt.client as mqtt
import atexit
import re
import time

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("http://192.168.0.7:81/stream")
# 공유 변수
latest_frame = None
latest_plate_coords = None  # (x_min, y_min, x_max, y_max)
latest_plate_text = ""
latest_plate_image = None


last_plate = None
last_time = 0
cooldown = 10 # 10초 이내 같은 번호판이 인식되었을 경우 무시

# MQTT 설정
MQTT_BROKER = "192.168.0.6"  # 또는 "192.168.0.x"
MQTT_PORT = 1883
MQTT_TOPIC = "car/number"
MQTT_USERNAME = "dahyun_raspi"
MQTT_PASSWORD = "0101"

# MQTT 클라이언트 준비
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()  # 비동기 전송을 위한 loop 시작

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

# Contours 에서 번호판 후보 찾기 -----------
# 1) box 크기로 필터링
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
# 2) 번호판 특성으로 필터링
# def find_chars(contour_list):
#     MAX_DIAG_MULTIPLYER = 4
#     MAX_ANGLE_DIFF = 12.0
#     MAX_AREA_DIFF = 0.4
#     MAX_WIDTH_DIFF = 0.6
#     MAX_HEIGHT_DIFF = 0.2
#     MIN_N_MATCHED = 4

#     matched_result_idx = []

#     for c1  in contour_list:
#         matched_contours_idx = []
#         for c2 in contour_list:
#             if c1['idx'] == c2['idx']: # 같은 contour 비교시 continue
#                 continue;

#             dx = abs(c1['cx'] - c2['cx'])
#             dy = abs(c1['cy'] - c2['cy'])

#             diagonal_length = np.sqrt(c1['w'] ** 2 + c1['h'] ** 2)

#             distance = np.linalg.norm(np.array([c1['cx'], c1['cy']]) - np.array([c2['cx'], c2['cy']]))
#             if dx == 0:
#                 angle_diff = 90
#             else:
#                 angle_diff = np.degrees(np.arctan(dy / dx))
#             area_diff = abs(c1['w'] * c1['h'] - c2['w'] * c2['h']) / (c1['w'] * c1['h'])
#             width_diff = abs(c1['w'] - c2['w']) / c1['w']
#             height_diff = abs(c1['h'] - c2['h']) / c1['h']
        
#             if distance < diagonal_length * MAX_DIAG_MULTIPLYER \
#             and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
#             and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
#                 matched_contours_idx.append(c2['idx'])
                
#         matched_contours_idx.append(c1['idx'])
        
#         if len(matched_contours_idx) < MIN_N_MATCHED:
#             continue
            
#         matched_result_idx.append(matched_contours_idx)
        
#         unmatched_contour_idx = []
#         for d4 in contour_list:
#             if d4['idx'] not in matched_contours_idx:
#                 unmatched_contour_idx.append(d4['idx'])
        
#         unmatched_contour = np.take(contour_list, unmatched_contour_idx)
        
#         recursive_contour_list = find_chars(unmatched_contour)
        
#         for idx in recursive_contour_list:
#             matched_result_idx.append(idx)
            
#         break
        
#     return matched_result_idx

def find_chars(contour_list):
    if not contour_list or len(contour_list) < 2:
        return []

    MAX_DIAG_MULTIPLYER = 4
    MAX_ANGLE_DIFF = 12.0
    MAX_AREA_DIFF = 0.4
    MAX_WIDTH_DIFF = 0.6
    MAX_HEIGHT_DIFF = 0.2
    MIN_N_MATCHED = 4

    matched_result_idx = []

    try:
        for c1 in contour_list:
            matched_contours_idx = []

            for c2 in contour_list:
                try:
                    if c1.get('idx') == c2.get('idx'):
                        continue

                    dx = abs(c1['cx'] - c2['cx'])
                    dy = abs(c1['cy'] - c2['cy'])

                    if c1['w'] == 0 or c1['h'] == 0:
                        continue

                    diagonal_length = np.sqrt(c1['w'] ** 2 + c1['h'] ** 2)
                    distance = np.linalg.norm(np.array([c1['cx'], c1['cy']]) - np.array([c2['cx'], c2['cy']]))

                    angle_diff = 90 if dx == 0 else np.degrees(np.arctan(dy / dx))

                    area1 = c1['w'] * c1['h']
                    area2 = c2['w'] * c2['h']
                    area_diff = abs(area1 - area2) / area1 if area1 != 0 else float('inf')

                    width_diff = abs(c1['w'] - c2['w']) / c1['w'] if c1['w'] != 0 else float('inf')
                    height_diff = abs(c1['h'] - c2['h']) / c1['h'] if c1['h'] != 0 else float('inf')

                    if distance < diagonal_length * MAX_DIAG_MULTIPLYER and \
                        angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF and \
                        width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                        matched_contours_idx.append(c2['idx'])

                except Exception as e:
                    print(f"[WARN] 비교 도중 예외 발생: {e}")
                    continue

            matched_contours_idx.append(c1['idx'])

            if len(matched_contours_idx) < MIN_N_MATCHED:
                continue

            matched_result_idx.append(matched_contours_idx)

            unmatched_contour_idx = [d.get('idx') for d in contour_list if d.get('idx') not in matched_contours_idx]

            if not unmatched_contour_idx:
                continue

            try:
                unmatched_contour = np.take(contour_list, unmatched_contour_idx)
            except Exception as e:
                print(f"[WARN] np.take 실패: {e}")
                continue

            recursive_contour_list = find_chars(unmatched_contour)

            for idx in recursive_contour_list:
                matched_result_idx.append(idx)

            break  # 하나만 찾고 종료

    except RecursionError:
        print("[ERROR] 재귀 한도 초과")

    except Exception as e:
        print(f"[ERROR] find_chars 전체 예외 발생: {e}")

    return matched_result_idx


# -------------------------------------------

# 프레임을 받아서 영상을 처리하는 함수
def process_frame():
    print("[DEBUG] process_frame 진입")  # ★ 꼭 넣어보세요
    global latest_frame, latest_plate_coords
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] 카메라 프레임 읽기 실패")
        return None
    
    # openCV 처리 로직 ====
    # 1. 영상 필터링 / 전처리 (흑백, 블러, 스레시홀딩 등)
    # 2. 윤곽선 탐지
    # 3. 번호판 후보 영역 찾기
    # 4. 번호판 위치가 결정되면 → latest_plate_coords 업데이트
    # 5. 처리된 전체 frame → latest_frame 에 저장
    # =====================

    # 1. 영상 필터링
    # 1-1. 가우시안 블러/흑백 이미지로 변환
    frame = cv2.flip(frame, 1)
    blur_frame = cv2.GaussianBlur(frame, (5, 5), sigmaX=0)
    gray_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2GRAY)
    # 1-2. Thresholding
    _, thresh_blur_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
    
    # 2. 윤곽선 탐지
    contours_blur, _ = cv2.findContours(thresh_blur_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    temp_result_blur = np.zeros(frame.shape, dtype=np.uint8)
    # 윤곽선 그리기
    # 아래 두 줄은 테스트 확인용 
    # cv2.drawContours(temp_result_blur, contours_blur, contourIdx=-1, color=(255,255,255))
    # cv2.imshow("t", temp_result_blur)
    
    # 3. 번호판 후보 영역 찾기
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

        # 검출 결과 저장
        latest_plate_coords = (x_min, y_min, x_max, y_max)
        # 번호판 전체 박스 그리기
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        plate_region = frame[y_min:y_max, x_min:x_max]

    latest_frame = frame
    print(f"[DEBUG] 최종 프레임 shape: {latest_frame.shape}")

    
    return latest_frame
    # 테스트 용
    # cv2.imshow("Frame", frame)
    # cv2.imshow("plate_region", flipped)
    # flipped = cv2.flip(plate_region, 1)

# 번호판 영역만 가져오기
def get_plate_region():
    global latest_plate_image
    if latest_frame is None or latest_plate_coords is None:
            return None

    x_min, y_min, x_max, y_max = latest_plate_coords
    latest_plate_image = latest_frame[y_min:y_max, x_min:x_max]
    return latest_plate_image 

# def OCR():
#     global latest_plate_image, latest_plate_text
#     gray = cv2.cvtColor(latest_plate_image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # 확대
#     blur = cv2.GaussianBlur(gray, (3, 3), 0)  # 노이즈 제거
#     _, thresh = cv2.threshold(blur, 121, 255, cv2.THRESH_BINARY)  # 이진화

#     # OCR
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Dev\Tool\Tesseract-OCR\tesseract.exe"
#     chars = pytesseract.image_to_string(thresh, lang='kor', config='--psm 7 --oem 0')
#     print(f"[DEBUG]📄 추출된 텍스트: {chars.strip()}")
#     latest_plate_text = chars.strip()
#     return latest_plate_text

def OCR():
    global latest_plate_text, latest_plate_image

    if latest_plate_image is None:
        print("[ERROR] OCR 실패: 번호판 이미지 없음")
        return ""

    try:
        gray = cv2.cvtColor(latest_plate_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blur, 145, 255, cv2.THRESH_BINARY)

        # OCR
        pytesseract.pytesseract.tesseract_cmd = r"C:\Dev\Tool\Tesseract-OCR\tesseract.exe"
        chars = pytesseract.image_to_string(thresh, lang='kor', config='--psm 7 --oem 0')
        plate_text = chars.strip()
        print(f"[DEBUG]📄 추출된 텍스트: {plate_text}")

        if plate_text:
            mqtt_client.publish(MQTT_TOPIC, plate_text)
            print(f"[MQTT] 전송 완료: {plate_text}")
        else:
            print("[INFO] 빈 텍스트, MQTT 전송 생략")

        return plate_text

    except Exception as e:
        print(f"[ERROR] OCR 처리 중 예외 발생: {e}")
        return ""

def cleanup():
    print("[INFO] 리소스 정리 중...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] 정리 완료. 종료.")

atexit.register(cleanup)