import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

button = 17
blue = 14
red = 15
green = 18

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

cnt = 0 	# 버튼이 클릭된 개수 저장
class Color:
	def __init__(self, b, r, g):
		self.b = b
		self.r = r
		self.g = g

	def setLed(self, tpl) :
		self.b, self.r, self.g = tpl
		GPIO.output(blue, self.b)
		GPIO.output(red, self.r)
		GPIO.output(green, self.g)

try:
	c = Color(0, 0, 0)
	while True:
		if not(GPIO.input(button)):
			cnt += 1
			cnt %= 4
			print(cnt)
			time.sleep(0.3) 	# 0.1 초 안에 수십 번 눌렀다고 인식하는 경우 방지
		if cnt == 1: 	# 파랑 
			c.setLed((1, 0, 0))
		elif cnt == 2:	# 빨강
			c.setLed((0, 1, 0))
		elif cnt == 3:	# 초록
			c.setLed((0, 0, 1))

except KeyboardInterrupt:
	GPIO.cleanup()

