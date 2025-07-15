# 인터럽트 실습3 - 버튼을 누른 시간에 따라 색깔 다르게 출력
# 1초 : 빨강
# 2초 : 파랑
# 3초 : 초록
# 4초 : 자홍
# 5초 : 청록
# 6초 : 노랑
# 7초 : 하양

import RPi.GPIO as GPIO
import time

swPin = 14
bluePin = 15
redPin = 18
greenPin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
        
def led_off():
    print("꺼짐")
    GPIO.output(bluePin, 0)
    GPIO.output(redPin, 0)
    GPIO.output(greenPin, 0)
	

def show_color_by_time(duration):
    print(f"눌린 시간: {duration:.2f}초")

    if duration >= 7.0:
        GPIO.output(redPin, 1)
        GPIO.output(greenPin, 1)
        GPIO.output(bluePin, 1)  # 하양
    elif duration >= 6.0:
        GPIO.output(redPin, 1)
        GPIO.output(greenPin, 1)  # 노랑
    elif duration >= 5.0:
        GPIO.output(bluePin, 1)
        GPIO.output(greenPin, 1)  # 청록  
    elif duration >= 4.0:  
        GPIO.output(redPin, 1)
        GPIO.output(bluePin, 1)  # 자홍
    elif duration >= 3.0:
        GPIO.output(greenPin, 1)
    elif duration >= 2.0:
        GPIO.output(bluePin, 1)
    elif duration >= 1.0:
        GPIO.output(redPin, 1)
    else:
        # print("1초 미만은 무시")
        GPIO.output(redPin, 1)
        GPIO.output(bluePin, 1)  # 자홍


    time.sleep(1)
    led_off()
		
try:
    while True:
        print("버튼 누르기를 기다리는 중...")
        GPIO.wait_for_edge(swPin, GPIO.FALLING)  # 누름
        time.sleep(0.05)
        if GPIO.input(swPin) == GPIO.LOW:  # 여전히 누르고 있다면
            start = time.time()
        
        GPIO.wait_for_edge(swPin, GPIO.RISING)  # 뗌
        end = time.time()

        duration = end - start
        show_color_by_time(duration)

except KeyboardInterrupt:
    GPIO.cleanup()
