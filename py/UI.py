
import pygame
import pygame.image
import pygame.transform

from py.setting import Font, Screen, Color, Save

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

font = Font().font

hpUI = pygame.image.load("pics/UI/heartIcon.png")
backpackUI = pygame.image.load("pics/UI/BackpackIcon.png")
clockUI = pygame.image.load("pics/UI/clockIcon.png")
clockUI = pygame.transform.scale(clockUI, (int(screen_width//5), screen_height//6))

menuIcon = pygame.image.load("pics/alt.png")

white = Color.white
black = Color.black
gray = Color.gray
dark_gray = Color.dark_gray

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

        self.show_inventory = False  # ← 인벤토리 표시 여부
        self.backpack_rect = backpackUI.get_rect(topleft=(0, 0))

    def render(self):
        screen.blit(backpackUI, (0, 0))

        screen.blit(clockUI, (screen_width - clockUI.get_width(), 0))
        screen.blit((font.render(f"D+ {self.day}", True, black)), (screen_width - 120, 0))
        screen.blit(self.timeUI, (screen_width - clockUI.get_width()*0.7, clockUI.get_width()*0.3))

        if self.show_inventory:
            self.draw_inventory()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                if self.backpack_rect.collidepoint(event.pos):
                    self.show_inventory = not self.show_inventory


    def update(self):
        self.sec += 1
        if self.sec >= 60:
            self.sec = 0
            self.min += 1
        if self.min >= 60:
            self.min = 0
            self.hou += 1

        time_str = f"{self.hou:02d}:{self.min:02d}"
        self.timeUI = font.render(time_str, True, white)

        

    def draw_inventory(self):
        ROWS, COLS = 3, 10
        SLOT_SIZE = 50
        SLOT_MARGIN = 5
        inventory_width = COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
        inventory_height = ROWS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN

        # 인벤토리 위치 (중앙 정렬)
        start_x = (screen_width - inventory_width) // 2
        start_y = (screen_height - inventory_height) // 2

        pygame.draw.rect(screen, black, (start_x, start_y, inventory_width, inventory_height)) 

        for row in range(ROWS):
            for col in range(COLS):
                x = start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                y = start_y + row * (SLOT_SIZE + SLOT_MARGIN)
                pygame.draw.rect(screen, gray, (x, y, SLOT_SIZE, SLOT_SIZE))         # 슬롯 배경
                pygame.draw.rect(screen, dark_gray, (x, y, SLOT_SIZE, SLOT_SIZE), 2) # 테두리

    