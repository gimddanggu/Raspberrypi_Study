import RPi.GPIO as GPIO
import time
import pygame

pygame.init()
screen = pygame.display.set_mode((300, 100))
pygame.display.set_caption("VNC 키보드 입력 테스트")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(f"키 눌림: {event.key}")
            if event.key == pygame.K_ESCAPE:
                running = False