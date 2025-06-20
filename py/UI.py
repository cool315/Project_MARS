
import pygame
import pygame.image
import pygame.transform

from py.setting import Font, Screen, Color, Save

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

font = Font().font
small_font = Font().small_font
item_font = Font().item_font


hpUI = pygame.image.load("pics/UI/heartIcon.png")
backpackUI = pygame.image.load("pics/UI/BackpackIcon.png")
clockUI = pygame.image.load("pics/UI/clockIcon.png")
clockUI = pygame.transform.scale(clockUI, (int(screen_width//5), screen_height//6))

menuIcon = pygame.image.load("pics/alt.png")

white = Color.white
black = Color.black
gray = Color.gray
dark_gray = Color.dark_gray

class UI:
    def __init__(self, save_data):
        if not Save().IsSAVE_FILE:
            self.sec = 0
            self.min = 0
            self.hou = 7
            self.day = 1
        else:
            self.sec = save_data['sec']
            self.min = save_data['min']
            self.hou = save_data['hou']
            self.day = save_data['day']
            
        self.timeUI = font.render("44:44", True, black)

        self.show_inventory = False  # ← 인벤토리 표시 여부
        self.backpack_rect = backpackUI.get_rect(topleft=(0, 0))

        self.placing_item = None
        self.placed_items = []  # 설치된 아이템들 저장

    def render(self, inventory):
        screen.blit(backpackUI, (0, 0))

        screen.blit(clockUI, (screen_width - clockUI.get_width(), 0))
        screen.blit((font.render(f"D+ {self.day}", True, black)), (screen_width - 120, 0))
        screen.blit(self.timeUI, (screen_width - clockUI.get_width()*0.7, clockUI.get_width()*0.3))

        # # 설치된 아이템들 그리기
        # for placed in self.placed_items:
        #     img = pygame.image.load(placed["item"]["buildingimage"]).convert_alpha()
        #     img = pygame.transform.scale(img, (50, 50))
        #     screen.blit(img, placed["position"])

        # # 마우스를 따라다니는 설치 준비 아이템
        if self.placing_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            img = pygame.image.load(self.placing_item["buildingimage"]).convert_alpha()
            img = pygame.transform.scale(img, (50, 50))
            img.set_alpha(128)  # 반투명 처리
            screen.blit(img, (mouse_x - 25, mouse_y - 25))  # 중심에 맞춰 위치

        if self.show_inventory:
            self.draw_inventory(inventory)


    def handle_event(self, event, inventory):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            if self.backpack_rect.collidepoint(event.pos):
                self.show_inventory = not self.show_inventory
                return  # 더 이상 처리하지 않음

            if self.show_inventory:
                # 인벤토리가 열려 있을 때 슬롯 클릭 감지
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

                for row in range(ROWS):
                    for col in range(COLS):
                        slot_x = slots_start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                        slot_y = slots_start_y + row * (SLOT_TOTAL_HEIGHT + SLOT_MARGIN)
                        slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
                        if slot_rect.collidepoint(mouse_x, mouse_y):
                            item = inventory[row][col]
                            if item is not None:
                                self.placing_item = item  # 아이템 선택
                                self.show_inventory = False  # 인벤토리 닫기
                            return

            else:
                # 설치 처리
                if self.placing_item:
                    self.placed_items.append({
                        "item": self.placing_item,
                        "position": event.pos
                    })
                    self.placing_item = None


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

    def draw_multiline_text(self, text, x, y, font, color, surface):
        lines = text.split('\n')  # 줄바꿈 기준으로 분리
        for i, line in enumerate(lines):
            rendered = font.render(line, True, color)
            surface.blit(rendered, (x, y + i * font.get_height()))
        
    def draw_inventory(self, inventory):
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

        # 배경 그리기
        pygame.draw.rect(screen, black, (start_x, start_y, background_width, background_height))

        # 슬롯들이 그려질 영역 시작 좌표 (배경 내부, 아래쪽 정렬)
        slots_start_x = start_x + padding
        slots_start_y = start_y + background_height - padding - inventory_height

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
                        tooltip_pos = (mouse_x, mouse_y)

        # 툴팁 표시
        if show_tooltip:
            lines = tooltip_text.split('\n')
            tooltip_font = small_font
            tooltip_line_height = tooltip_font.get_height()
            tooltip_width = max(tooltip_font.size(line)[0] for line in lines)
            tooltip_height = len(lines) * tooltip_line_height

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