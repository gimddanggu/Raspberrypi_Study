import cv2
import time
import video_processor  # 모듈 이름에 맞게 변경하세요

# cap = cv2.VideoCapture("http://192.168.0.7:81/stream")
cap = cv2.VideoCapture(0)


# 영상 처리 반복
def main():
    print("[INFO] 테스트 시작 - ESC 키를 누르면 종료됩니다.")
    while True:
        frame = video_processor.process_frame()
        if frame is None:
            print("[WARN] 프레임 수신 실패")
            time.sleep(0.5)
            continue
        
        # OpenCV 창으로 결과 보기
        cv2.imshow("License Plate Detection", frame)

        # ESC 키 누르면 종료
        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()