import RPi.GPIO as GPIO
import time 
# GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
segmentPin = [12, 16, 17, 15, 23, 20, 21]
# [12:a, 16:b, 17:c, 15:d, 23:e, 20, 21] 27:dot
digits = [
	[1, 1, 1, 1, 1, 1, 0], 
	[0, 1, 1, 0, 0, 0, 0],
	[1, 1, 0, 1, 1, 0, 1],
	[1, 1, 1, 1, 0, 0, 1],
	[0, 1, 1, 0, 0, 1, 1], # 4
	[1, 0, 1, 1, 0, 1, 1], # 5
	[1, 0, 1, 1, 1, 1, 1], # 6
	[1, 1, 1, 0, 0, 1, 0], # 7 
	[1, 1, 1, 1, 1, 1, 1], # 8
	[1, 1, 1, 1, 0, 1, 1]  # 9
]
# 핀 설정
for i in range(0, 7):
	GPIO.setup(segmentPin, GPIO.OUT)

# 핀 초기화
def pinReset():
	for i in range(0, 7):
		GPIO.output(segmentPin[i], 0)

# # 숫자 출력
for num in range(0, 10):
	print(num)
	for i in range(0, 7):
		GPIO.output(segmentPin[i], digits[num][i])
	time.sleep(1)
	pinReset()

# 테스트 코드,
# for i in segmentPin:
# 	GPIO.output(i, 1)
# 	time.sleep(1)
# 	GPIO.output(i, 0)
# pinReset()

