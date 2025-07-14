import RPi.GPIO as GPIO
import time

piezoPin = 18

Melody = [131, 146, 164, 175, 196, 220, 247, 262]

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)
# 해당핀에 440Hz 출력
sound = GPIO.PWM(piezoPin, 440)

try:
	while True:
		sound.start(50) # 듀티비 50% PWN 시작
		for i in range(0, len(Melody)):
			sound.ChangeFrequency(Melody[i])		# 주파수 변경
			time.sleep(0.3)
		sound.stop()		# PWM 중지
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()

