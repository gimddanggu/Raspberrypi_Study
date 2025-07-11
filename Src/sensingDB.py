import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import mysql.connector

# DB 연결 설정
conn = mysql.connector.connect(
	host="localhost",
	user="dahyun",
	password="0101",
	database="testdb"
)

cursor = conn.cursor()

GPIO.setmode(GPIO.BCM)

dht = adafruit_dht.DHT11(board.D23)

while True:
	try:
		temp = dht.temperature
		humi = dht.humidity
		#INSERT
		query = "INSERT INTO sensing_data (temperature, humidity) VALUES (%s, %s)"
		cursor.execute(query, (temp, humi))
		conn.commit()
		print(f"Temp:{temp} Humi: {humi}", temp, humi)
		time.sleep(3)
	except RuntimeError as error:
		print(error.args[0])
	except KeyboardInterrupt:
		GPIO.cleanup()
		break;


cursor.close()
conn.close()
