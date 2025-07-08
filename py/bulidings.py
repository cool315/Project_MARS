import pygame
import pygame.image
import pygame.transform

from py.setting import Screen, Font, Color, resource_path

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
        self.IsPlaced = IsPlaced
        self.IsConstructed = None

    def render(self):
        if self.IsPlaced and self.IsConstructed:
            screen.blit(self.img, (self.x, self.y))

    def update(self):
        if self.IsPlaced and self.IsConstructed:
            # rect 위치 동기화
            self.rect.topleft = (self.x, self.y)

            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                tooltip_surface = small_font.render("e키를 눌러서 입장", True, black)
                screen.blit(tooltip_surface, (self.rect.right + 10, self.rect.top))
                        

class Dome(BaseBuilding):
    def __init__(self, x, y, IsConstructed):
        super().__init__(x, y, False)
        self.img = pygame.image.load(resource_path("pics/buildings/domeBuilding1.png"))
        self.img = pygame.transform.scale(self.img, (screen_height // 5, screen_height // 5))
        self.rect = self.img.get_rect(topleft=(x, y))
        self.IsConstructed = IsConstructed

class spaceShip(BaseBuilding):
    def __init__(self):
        super().__init__(screen_width // 2, screen_height // 2, True)
        self.img = pygame.image.load(resource_path("pics/buildings/SpaceShip.png"))
        self.img = pygame.transform.scale(self.img, (screen_width // 10, screen_height // 4))
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.IsConstructed = True
        self.IsDestroyed = False

BUILDING_CLASSES = {
    "dome": Dome,
    "spaceship": spaceShip,
}