import RPi.GPIO as GPIO
import pygame
import time

pygame.init()
screen = pygame.display.set_mode((300, 100))
pygame.display.set_caption("피아노 부저")

buzzer_pin = 18
GPIO.setmode(GPIO.BCM)

GPIO.setup(buzzer_pin, GPIO.OUT)
sound = GPIO.PWM(buzzer_pin, 440)

def play_piano(key):
    k_map = {
        49: 65.5, # 1: 도
        50: 73.5, # 2: 레
        51: 82.5,
        52: 87.3,
        53: 98,
        54: 110,
        55: 123.5,
        56: 131.3,
    }

    if key in k_map:
        sound.start(50)
        sound.ChangeFrequency(k_map[key])
        time.sleep(0.5)
        sound.stop()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(f"키 눌림: {event.key}")
            play_piano(event.key)
            if event.key == pygame.K_ESCAPE:
                running = False

GPIO.cleanup()
