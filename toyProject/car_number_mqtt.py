import paho.mqtt.client as mqtt

topic = "car/number"

# 연결: 0, 연결 거부: 1, 인증 실패: 5
def on_connect(client, userdata, flags, rc):
	print(f"연결됨코드: {rc}")
	client.subscribe(topic)

def on_message(client, userdata, msg):
	print(f"[번호판] {msg.payload.decode()}")

client = mqtt.Client()

try:
	client.username_pw_set(username="dahyun_raspi", password="0101")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)
	client.loop_forever()

except Exception as e:
	print(f"브로커 연결실패, 코드: {e}")

finally:
	client.disconnect()

