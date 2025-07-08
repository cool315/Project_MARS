
import pygame
import pygame.image
import pygame.transform

from py.setting import Font, Screen, Color, Save, resource_path
from py.bulidings import BUILDING_CLASSES

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

font = Font().font
small_font = Font().small_font
item_font = Font().item_font

hpUI = pygame.image.load(resource_path("pics/UI/heartIcon.png"))
backpackUI = pygame.image.load(resource_path("pics/UI/BackpackIcon.png"))
clockUI = pygame.image.load(resource_path("pics/UI/clockIcon.png"))
clockUI = pygame.transform.scale(clockUI, (int(screen_width//5), screen_height//6))
backpackActionUI = pygame.transform.scale(
    pygame.image.load(resource_path("pics/UI/backpackIcon.png")),
    (screen_width // 50, screen_width // 50)
)
exitActionUI = pygame.transform.scale(
    pygame.image.load(resource_path("pics/UI/ExitIcon.png")),
    (screen_width // 50, screen_width // 50)
)

white = Color.white
black = Color.black
gray = Color.gray
dark_gray = Color.dark_gray
red = Color.red

ROWS, COLS = 3, 10
SLOT_SIZE = 50
TEXT_HEIGHT = 16
SLOT_MARGIN = 10
SLOT_TOTAL_HEIGHT = SLOT_SIZE + TEXT_HEIGHT

inventory_width = COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
inventory_height = ROWS * (SLOT_TOTAL_HEIGHT + SLOT_MARGIN) - SLOT_MARGIN
padding = 40

background_width = inventory_width + padding * 2
background_height = inventory_height + padding * 6

start_x = (screen_width - background_width) // 2
start_y = (screen_height - background_height) // 2

slots_start_x = start_x + padding
slots_start_y = start_y + background_height - padding - inventory_height

class UI:
    def __init__(self, save_data, inventoryM):
        self.save_data = save_data
        self.inventoryM = inventoryM

        if not Save().IsSAVE_FILE:
            self.sec = 0
            self.min = 0
            self.hou = 7
            self.day = 1
        else:
            self.sec = self.save_data['sec']
            self.min = self.save_data['min']
            self.hou = self.save_data['hou']
            self.day = self.save_data['day']
            
        self.timeUI = font.render("44:44", True, black)

        self.show_inventory = False  # ← 인벤토리 표시 여부
        self.backpack_rect = backpackUI.get_rect(topleft=(0, 0))
        self.exit_button_rect = pygame.Rect(300, 250, 200, 60)  # x, y, 너비, 높이
        self.backpackAc_rect = backpackActionUI.get_rect(topleft=(0,0))
        self.exitAc_rect = exitActionUI.get_rect(topleft=(0,0))

        self.domeX = screen_width // 2
        self.domeY = screen_height // 2
        self.IsDomePlaced = False

        self.selected_item = None  # 선택된 아이템

        self.actionbar = ["inventory", "quest", "exit"]
        self.selected_action = 0

    def save_update(self):
        self.sec = self.save_data['sec']
        self.min = self.save_data['min']
        self.hou = self.save_data['hou']
        self.day = self.save_data['day']

    def render(self, background):
        self.draw_playerUI(background)

        # 마우스를 따라다니는 설치 준비 아이템
        if not self.selected_item == None and self.selected_item['IsBuilding']:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            img = pygame.image.load(resource_path(self.selected_item["placeimage"])).convert_alpha()
            img = pygame.transform.scale(img, (screen_height // 5, screen_height // 5))
            img.set_alpha(128)  # 반투명 처리
            screen.blit(img, (mouse_x - img.get_width() // 2, mouse_y - img.get_height() // 2))  # 중심에 맞춰 위치
        elif not self.selected_item == None and self.selected_item['IsSeed']:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            img = pygame.image.load(resource_path(self.selected_item["placeimage"] + "1.png")).convert_alpha()
            img = pygame.transform.scale(img, (screen_height // 20, screen_height // 20))
            img.set_alpha(128)  # 반투명 처리
            screen.blit(img, (mouse_x - img.get_width() // 2, mouse_y - img.get_height() // 2))  # 중심에 맞춰 위치

        if self.show_inventory:
            self.draw_basic_menu()
            if self.actionbar[self.selected_action] == "inventory":
                self.draw_inventory(self.inventoryM.inventory)
            elif self.actionbar[self.selected_action] == "exit":
                self.draw_exit()

    def handle_event(self, event, dome, plant, background):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            if self.backpack_rect.collidepoint(event.pos):
                self.show_inventory = not self.show_inventory
                return  # 더 이상 처리하지 않음

            if self.backpackAc_rect.collidepoint(event.pos):
                self.selected_action = 0
            elif self.exitAc_rect.collidepoint(event.pos):
                self.selected_action = 2

            if self.show_inventory:
                # 인벤토리가 열려 있을 때 슬롯 클릭 감지
                self.selected_item = None  # 아이템 선택 초기화

                for row in range(ROWS):
                    for col in range(COLS):
                        slot_x = slots_start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                        slot_y = slots_start_y + row * (SLOT_TOTAL_HEIGHT + SLOT_MARGIN)
                        slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
                        if slot_rect.collidepoint(mouse_x, mouse_y):
                            item = self.inventoryM.inventory[row][col]
                            if item is not None:
                                self.selected_item = item
                                self.selected_item_pos = (row, col)
                                if self.selected_item['IsBuilding']:
                                    self.show_inventory = False  # 인벤토리 닫기
                                elif self.selected_item['IsSeed'] and background.backgroundName == "GreenHouse":
                                    self.show_inventory = False  # 인벤토리 닫기
                            return
            else:
                if self.selected_item is not None:
                    if self.selected_item['IsBuilding']:
                        if self.selected_item['placeType'] == "dome":
                            dome.IsConstructed = True
                            dome.IsPlaced = True
                            x, y = pygame.mouse.get_pos()
                            dome.x, dome.y = x - dome.img.get_height() // 2, y - dome.img.get_height() // 2

                            sel_row, sel_col = self.selected_item_pos
                            self.inventoryM.inventory[sel_row][sel_col]["count"] -= 1

                            self.selected_item = None  # 아이템 선택 해제
                            self.selected_item_pos = None
                    elif self.selected_item['IsSeed']:
                        if(plant.planting_click(pygame.mouse.get_pos(), self.selected_item['placeType'])):
                            sel_row, sel_col = self.selected_item_pos
                            self.inventoryM.inventory[sel_row][sel_col]["count"] -= 1

                            self.selected_item = None  # 아이템 선택 해제
                            self.selected_item_pos = None
    
    def update(self):
        self.sec += 1
        if self.sec >= 60:
            self.sec = 0
            self.min += 1
        if self.min >= 60:
            self.min = 0
            self.hou += 1
        if self.hou >= 24 & self.min >= 37:
            self.hou = 1
            self.min = 0

        time_str = f"{self.hou:02d}:{self.min:02d}"
        self.timeUI = font.render(time_str, True, white)

        for row in range(ROWS):
            for col in range(COLS):
                item = self.inventoryM.inventory[row][col]
                if item is not None:
                    if item['count'] <= 0:
                        self.inventoryM.inventory[row][col] = None  # 아이템 제거

    def draw_multiline_text(self, text, x, y, font, color, surface):
        lines = text.split('\n')  # 줄바꿈 기준으로 분리
        for i, line in enumerate(lines):
            rendered = font.render(line, True, color)
            surface.blit(rendered, (x, y + i * font.get_height()))
    
    def draw_playerUI(self, background):
        screen.blit(backpackUI, (0, 0))

        screen.blit(clockUI, (screen_width - clockUI.get_width(), 0))
        if background == "SpaceshipInside" or background == "DomeInside":
            screen.blit((font.render(f"D+ {self.day}", True, white)), (screen_width - 120, 0))
        else:
            screen.blit((font.render(f"D+ {self.day}", True, black)), (screen_width - 120, 0))
        screen.blit(self.timeUI, (screen_width - clockUI.get_width()*0.7, clockUI.get_width()*0.3))

    def draw_basic_menu(self):
        pygame.draw.rect(screen, black, (start_x, start_y, background_width, background_height))

        backpack_pos = (start_x, start_y - backpackActionUI.get_height())
        exit_pos = (start_x + backpackActionUI.get_width(), start_y - exitActionUI.get_height())

        self.backpackAc_rect.topleft = backpack_pos
        self.exitAc_rect.topleft = exit_pos  # ← 여기 추가!

        screen.blit(backpackActionUI, backpack_pos)
        screen.blit(exitActionUI, exit_pos)

    def draw_exit(self):
        pygame.draw.rect(screen, white, self.exit_button_rect, border_radius=10)

        # 텍스트 그리기
        text_surface = font.render("종료하기", True, red)
        text_rect = text_surface.get_rect(center=self.exit_button_rect.center)
        screen.blit(text_surface, text_rect)

    def draw_inventory(self, inventory):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        show_tooltip = False
        tooltip_text = ""
        tooltip_pos = (0, 0)

        for row in range(ROWS):
            for col in range(COLS):
                slot_x = slots_start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                slot_y = slots_start_y + row * (SLOT_TOTAL_HEIGHT + SLOT_MARGIN)
                slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)

                pygame.draw.rect(screen, gray, slot_rect)
                pygame.draw.rect(screen, dark_gray, slot_rect, 2)

                item = inventory[row][col]
                if item is not None:
                    # 이미지 출력
                    item_image = pygame.image.load(item['image'])
                    item_image = pygame.transform.scale(item_image, (SLOT_SIZE, SLOT_SIZE))
                    screen.blit(item_image, (slot_x, slot_y))

                    # 이름 출력
                    name_surface = item_font.render(item['name'], True, white)
                    name_x = slot_x + (SLOT_SIZE - name_surface.get_width()) // 2
                    name_y = slot_y + SLOT_SIZE + 2
                    screen.blit(name_surface, (name_x, name_y))

                    # 마우스가 슬롯 위에 있다면 툴팁 표시 준비
                    if slot_rect.collidepoint(mouse_x, mouse_y):
                        show_tooltip = True
                        tooltip_text = item["description"]
                        count = item["count"]
                        tooltip_pos = (mouse_x, mouse_y)

        # 툴팁 표시
        if show_tooltip:
            lines = tooltip_text.split('\n')
            tooltip_font = small_font
            tooltip_line_height = tooltip_font.get_height()
            tooltip_width = max(tooltip_font.size(line)[0] for line in lines)
            tooltip_height = (len(lines) + 1) * tooltip_line_height

            tooltip_bg = pygame.Rect(
                tooltip_pos[0] + 10,
                tooltip_pos[1] + 10,
                tooltip_width + 20,
                tooltip_height + 10
            )

            pygame.draw.rect(screen, (50, 50, 50), tooltip_bg)  # 배경
            pygame.draw.rect(screen, white, tooltip_bg, 1)      # 테두리

            # 텍스트 줄 단위로 출력
            self.draw_multiline_text(
                tooltip_text,
                tooltip_pos[0] + 20,
                tooltip_pos[1] + 15,
                tooltip_font,
                white,
                screen
            ) 
            screen.blit(
                tooltip_font.render(f"{count}개", True, black),
                (tooltip_pos[0] + 20, tooltip_height - tooltip_pos[1])
            )