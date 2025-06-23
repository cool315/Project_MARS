import pygame
import pygame.image
import pygame.transform

from py.setting import Screen, Font, Color

screen = Screen().screen
screen_width = Screen().screen_width
screen_height = Screen().screen_height

small_font = Font().small_font

black = Color().black

class BaseBuilding:
    def __init__(self, x, y, IsPlaced):
        self.x = x
        self.y = y
        self.img = None  # 하위 클래스에서 설정
        self.rect = None
        self.IsPlaced = IsPlaced  # 건물이 설치되었는지 여부

    def render(self):
        if self.IsPlaced:
            screen.blit(self.img, (self.x, self.y))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            tooltip_surface = small_font.render("e키를 눌러서 입장", True, black)
            screen.blit(tooltip_surface, (self.rect.right + 10, self.rect.top))

class Dome(BaseBuilding):
    def __init__(self, x, y, IsPlaced):
        super().__init__(x, y, IsPlaced)
        self.img = pygame.image.load("pics/buildings/domeBuilding1.png")
        self.img = pygame.transform.scale(self.img, (screen_height // 5, screen_height // 5))
        self.rect = self.img.get_rect(topleft=(x, y))

class spaceShip(BaseBuilding):
    def __init__(self):
        super().__init__(screen_width // 2, screen_height // 2, True)
        self.img = pygame.image.load("pics/buildings/SpaceShip.png")
        self.img = pygame.transform.scale(self.img, (screen_width // 10, screen_height // 4))
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

BUILDING_CLASSES = {
    "dome": Dome,
    "spaceship": spaceShip,
}