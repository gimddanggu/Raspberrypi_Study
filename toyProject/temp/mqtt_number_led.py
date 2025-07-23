import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import re

# 사이렌 울리는 함수
def siren():
            for freq in range(600, 1600, 20):
                sound.ChangeFrequency(freq)
                time.sleep(0.01)
                
            for freq in range(1600, 600, -20):
                sound.ChangeFrequency(freq)

# GPIO 설정
GREEN_PIN = 21
RED_PIN = 20
PIEZO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(PIEZO_PIN, GPIO.OUT)

# sound = GPIO.PWM(PIEZO_PIN, 440)


# MQTT 브로커 정보
MQTT_BROKER = "localhost"  # 또는 IP 주소 (예: "192.168.0.10")
MQTT_PORT = 1883
MQTT_TOPIC = "car/number"

# 인증 정보
MQTT_USERNAME = "dahyun_raspi"
MQTT_PASSWORD = "0101"
reg_car_number = ["2704"]

def is_valid_plate(plate):
    return re.fullmatch(r"\d{2,3}[가-힣]\d{4}", plate) is not None

# 콜백 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT 연결 성공")
        client.subscribe(MQTT_TOPIC)
        GPIO.output(PIEZO_PIN, GPIO.LOW)
    else:
        print(f"MQTT 연결 실패: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"번호: {payload}")

    if not is_valid_plate(payload):
        print("잘못된 번호판 형식입니다. (무시)")
        return

    last_four_num = payload[-4:]
    # 등록된 차량이 들어왔다면
    if last_four_num in reg_car_number:
        print(GPIO.input(PIEZO_PIN))
        
        print("등록된 차량입니다")
        time.sleep(1)
        GPIO.output(GREEN_PIN, GPIO.LOW)

        # 원래 차량 등록된 차량이면 7segment 4개에 차량번호 보이게 하려고 했는데
        # 카메라 이슈로 시간이 너무 오래 걸렸어요...
        # 대신 한 개짜리 7segment 영상 첨부합니다!
    else:
        GPIO.output(RED_PIN, GPIO.HIGH)
        print("등록되지 않은 차량입니다.")
        # siren()

        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.LOW)

        


# MQTT 클라이언트 설정
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# 브로커 연결
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("종료합니다.")

finally:
    GPIO.cleanup()

