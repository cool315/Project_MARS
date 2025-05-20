
import pygame

from py.setting import Font, Screen, Color

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

menuUI = pygame.image.load("pics/alt.png")
hpUI = pygame.image.load("pics/UI/heartIcon.png")
backpackUI = pygame.image.load("pics/UI/BackpackIcon.png")

class UI:
    def __init__(self):
        pass
        
    def render(self):
        screen.blit(menuUI, (screen_width - menuUI.get_width(), 0))
        screen.blit(backpackUI, (0, 0))
    