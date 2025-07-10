import RPi.GPIO as GPIO
import time

button = 17
blue = 14
red = 15
green = 18

cnt = 0
cooldownTime = 0.8 # 0.8초 이상 입력 없으면 led 결과 출력
lastPressTime = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 풀 다운 방식
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

class Color():
    def __init__(self, b, r, g):
        self.b = b
        self.r = r
        self.g = g
    
    def 

try:
    c = Color()
    while 1:
        if (GPIO.input(button) and cnt == 0 and lastPressTime == 0):
            lastPressTime = time.time()
        elif (cnt > 0 and time.time() - lastPressTime < cooldownTime):
            cnt += 1
        
        if (time.time() - lastPressTime > cooldownTime):
            if cnt == 1:
                

except KeyboardInterrupt:
    GPIO.cleanup()