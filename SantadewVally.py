import pygame
import sys
import json
import os

from player import Player
from opening import Opening
from setting import Color, Screen, clock, Font

#초기 설정
pygame.init()
pygame.display.set_caption("산타듀밸리")
screen = Screen.screen
screen_width, screen_height = (Screen.screen_width, Screen.screen_height)

player = Player(screen_width // 2, screen_height // 2)

Opening().show_caption()

# 배경
background = pygame.image.load("pics/backgrounds/marsBackground1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    player.update()

    #화면 그리기
    screen.blit(background, (0, 0))
    player.render(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()