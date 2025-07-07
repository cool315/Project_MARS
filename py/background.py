import pygame
import pygame.image

from py.setting import Screen, Font, Color

screen = Screen().screen
screen_width, screen_height = Screen().screen_width, Screen().screen_height

small_font = Font().small_font

black = Color.black
white = Color.white

class backgroundElementControl:
    def __init__(self, background):
        self.backgroundName = background

        self.background = pygame.image.load("pics/backgrounds/marsBackground1.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        self.backgroundItems = None

        self.bed_rect = None  # 침대 위치 저장용
        self.bed_x, self.bed_y = 0, 0

        self.monitor_rect = None

        self.is_inside_spaceship = False
        self.is_inside_dome = False

    def render(self):
        screen.blit(self.background, (0, 0))

        if self.backgroundItems:
            for item, x, y in self.backgroundItems:
                screen.blit(item, (x, y))

    def update(self):
        if self.backgroundName == "DomeInside":
            # 침대 위에 마우스를 올렸는지 감지
            mouse_pos = pygame.mouse.get_pos()
            if self.bed_rect and self.bed_rect.collidepoint(mouse_pos):
                tooltip = small_font.render("e키를 눌러서 잠자기", True, black)
                screen.blit(tooltip, (self.bed_rect.right + 10, self.bed_rect.top))
            elif self.monitor_rect and self.monitor_rect.collidepoint(mouse_pos):
                tooltip = small_font.render("e키를 눌러서 컴퓨터 들어가기", True, white)
                screen.blit(tooltip, (self.bed_rect.right + 10, self.bed_rect.top))

    def outSide(self):
        self.background = pygame.image.load("pics/backgrounds/marsBackground1.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.backgroundName = "outside"

        self.is_inside_spaceship = False
        self.is_inside_dome = False

        self.backgroundItems = None

    def InsideSpaceShip(self):
        self.background = pygame.image.load("pics/backgrounds/SpaceShipInside.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.backgroundName = "SpaceshipInside"

        self.is_inside_spaceship = True

        self.backgroundItems = None

    def InsideDome(self):
        self.background = pygame.image.load("pics/backgrounds/DomeInside.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.backgroundName = "DomeInside"

        self.is_inside_dome = True

        self.bed = pygame.image.load("pics/items/bed.png")
        self.bed = pygame.transform.scale(self.bed, (screen_width // 10, screen_height // 10))
        self.bed_x = screen_width // 2
        self.bed_y = screen_height - screen_height // 10 - self.bed.get_height()
        self.bed_rect = self.bed.get_rect(topleft=(self.bed_x, self.bed_y))  # 침대 영역 저장

        self.monitor = pygame.image.load("pics/items/monitor.png")
        self.monitor = pygame.transform.scale(self.monitor, (screen_width // 10, screen_height // 10))
        monitor_x = screen_width // 2
        monitor_y = screen_height // 10 + self.monitor.get_height()
        self.monitor_rect = self.bed.get_rect(topleft=(monitor_x, monitor_y))

        self.backgroundItems = [
            (self.bed, self.bed_x, self.bed_y),
            (self.monitor, monitor_x, monitor_y)
        ]

    def computer(self):
        self.background = pygame.image.load("pics/backgrounds/windowXp.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.backgroundName = "Computer"

        self.is_inside_dome = False

        self.backgroundItems = None

    def insideGreenHouse(self):
        self.background = pygame.image.load("pics/backgrounds/PlantingRoom.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.backgroundName = "GreenHouse"

        self.is_inside_dome = False

        self.backgroundItems = None
        
