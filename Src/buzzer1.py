# import RPi.GPIO as GPIO
# import time

# buzzerPin = 18

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(buzzerPin, GPIO.OUT)

# try:
# 	GPIO.output(buzzerPin, GPIO.HIGH)
# 	print("buzzer on")
# 	time.sleep(1)
# 	GPIO.output(buzzerPin, GPIO.LOW)
# 	print("buzzer off")

# except KeyboardInterrupt:
# 	print("end")
# finally:
# 	GPIO.cleanup()

import RPi.GPIO as GPIO
import time

buzzerPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)

# PWM 설정: 1000Hz로 설정 (1kHz는 잘 들리는 음)
pwm = GPIO.PWM(buzzerPin, 1000)
pwm.start(50)  # 듀티비 50%로 시작

try:
    print("buzzer on")
    time.sleep(1)  # 1초 동안 소리 출력
    pwm.stop()
    print("buzzer off")

except KeyboardInterrupt:
    pwm.stop()
    print("Stopped by user")

finally:
    GPIO.cleanup()

