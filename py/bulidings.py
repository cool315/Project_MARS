import pygame
import pygame.image
import pygame.transform

from py.setting import Screen, Font, Color

screen = Screen().screen
screen_width = Screen().screen_width
screen_height = Screen().screen_height

small_font = Font().small_font

black = Color().black

class spaceShip:
    def __init__(self):
        self.img = pygame.image.load("pics/buildings/SpaceShip.png")
        self.img = pygame.transform.scale(self.img, (screen_width // 8, screen_height//4))

        self.x = screen_width // 2
        self.y = screen_height // 2

        self.image_rect = self.img.get_rect(topleft=(self.x, self.y))

    def render(self):
        screen.blit(self.img, (self.x, self.y))
        self.image_rect.topleft = (self.x, self.y)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        # 마우스가 이미지 위에 있을 경우
        if self.image_rect.collidepoint(mouse_pos):
            tooltip_surface = small_font.render("e키를 눌러서 입장", True, black)
            screen.blit(tooltip_surface, (self.image_rect.right + 10, self.image_rect.top))

class Dome:
    def __init__(self):
        self.img = pygame.image.load("pics/buildings/domeBuilding1.png")