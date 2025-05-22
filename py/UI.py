
import pygame
import pygame.image

from py.setting import Font, Screen, Color, Save

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

font = Font().font

hpUI = pygame.image.load("pics/UI/heartIcon.png")
backpackUI = pygame.image.load("pics/UI/BackpackIcon.png")
clockUI = pygame.image.load("pics/UI/clockIcon.png")

menuIcon = pygame.image.load("pics/alt.png")

white = Color.white
black = Color.black

if not Save().IsSAVE_FILE:
    sec = 0
    min = 0
    hou = 7
    day = 1

    time = f"{hou} : {min}"
else:
    pass

class UI:
    def __init__(self):
        if not Save().IsSAVE_FILE:
            self.sec = 0
            self.min = 0
            self.hou = 7
            self.day = 1
        else:
            pass
        self.timeUI = font.render("44:44", True, black)

    def render(self):
        screen.blit(backpackUI, (0, 0))
        screen.blit(clockUI, (screen_width - clockUI.get_width(), 0))
        screen.blit(self.timeUI, (screen_width - self.timeUI.get_width(), 0))

    def update(self):
        self.sec += 1
        if self.sec >= 60:
            self.sec = 0
            self.min += 1
        if self.min >= 60:
            self.min = 0
            self.hou += 1

        time_str = f"{self.hou:02d}:{self.min:02d}"
        self.timeUI = font.render(time_str, True, black)


    