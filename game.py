import pygame
import sys
import json
import os

from py.player import Player

# 초기 설정
pygame.init()

# 저장 파일 경로
SAVE_FILE = "save/save_data.json"

# 인벤토리 설정
inventory_rows, inventory_cols = 4, 9
inventory_slots = [None] * (inventory_rows * inventory_cols)

# 버튼 위치 정의
continue_btn = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 50, 300, 80)
restart_btn = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 70, 300, 80)

def load_item_image(item_name):
    path = f"pics/UI/items/{item_name}.png"
    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (42, 42))
    return None

def load_game_data():
    if not os.path.exists(SAVE_FILE):
        return {
            "prologue_seen": False,
            "player_position": default_position,
            "inventory_slots": [
                {
                    "name": "돔",
                    "image": "pics/UI/items/dome.png",
                    "quantity": 1,
                }
            ]
        }
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 게임 데이터 저장 및 불러오기

def save_game_data(data):
    data["player_position"] = (char_x, char_y)
    data["inventory"] = inventory_slots
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def reset_game_data():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


# UI 함수들

def draw_button(text, rect, color, font):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, white)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def show_load_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if continue_btn.collidepoint((mx, my)):
                    return "continue"
                elif restart_btn.collidepoint((mx, my)):
                    return "restart"

        screen.fill(black)
        title = font.render("파일 불러오기", True, white)
        screen.blit(title, title.get_rect(center=(screen_width / 2, screen_height / 4)))
        draw_button("이어하기", continue_btn, gray, small_font)
        draw_button("다시 시작", restart_btn, gray, small_font)
        pygame.display.flip()
        clock.tick(fps)

def show_warning_message():
    warning_text = "게임 데이터를 초기화하고 새로 시작합니다. 계속 하시겠습니까?"
    yes_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 70, 140, 50)
    no_button = pygame.Rect(screen_width // 2 + 10, screen_height // 2 + 70, 140, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if yes_button.collidepoint((mx, my)):
                    return True
                elif no_button.collidepoint((mx, my)):
                    return False

        screen.fill(black)
        warning_label = small_font.render(warning_text, True, white)
        screen.blit(warning_label, (screen_width // 2 - warning_label.get_width() // 2, screen_height // 2 - 50))
        draw_button("예", yes_button, gray, small_font)
        draw_button("아니오", no_button, gray, small_font)
        pygame.display.flip()
        clock.tick(fps)

# 게임 시작
char_x, char_y = default_position
char_speed = 5

# 인벤토리 아이콘 불러오기
inventory_icon = pygame.image.load("pics/UI/BackpackIcon.png")
inventory_icon = pygame.transform.scale(inventory_icon, (60, 60))
inventory_button_rect = pygame.Rect(10, 10, 60, 60)

direction = "down"
inventory_open = False

# 불러오기/시작 처리
game_data = load_game_data()
choice = show_load_menu()
if choice == "restart":
    if show_warning_message():
        reset_game_data()
        game_data = {}
        save_game_data({
            "prologue_seen": False, 
            "player_position": default_position, 
            "inventory": inventory_slots
        })
        char_x, char_y = default_position
    else:
        char_x, char_y = game_data.get("player_position", default_position)
elif choice == "continue":
    char_x, char_y = game_data.get("player_position", default_position)

inventory_slots = game_data.get("inventory", inventory_slots)

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if inventory_button_rect.collidepoint((mx, my)):
                inventory_open = not inventory_open

    screen.blit(inventory_icon, inventory_button_rect)

    if inventory_open:
        pygame.draw.rect(screen, (30, 30, 30), (200, 100, 600, 400))
        pygame.draw.rect(screen, white, (200, 100, 600, 400), 3)
        label = small_font.render("인벤토리", True, white)
        screen.blit(label, (210, 110))

        for row in range(inventory_rows):
            for col in range(inventory_cols):
                idx = row * inventory_cols + col
                slot_x = 220 + col * 60
                slot_y = 160 + row * 60
                pygame.draw.rect(screen, gray, (slot_x, slot_y, 50, 50))
                pygame.draw.rect(screen, white, (slot_x, slot_y, 50, 50), 2)

                item = inventory_slots[idx]
                if item:
                    item_img = load_item_image(item["name"])
                    if item_img:
                        screen.blit(item_img, (slot_x + 4, slot_y + 4))

                    count_text = small_font.render(str(item.get("count", 1)), True, white)
                    screen.blit(count_text, (slot_x + 25, slot_y + 25))

                    if "durability" in item:
                        bar_width = int(40 * (item["durability"] / 100))
                        pygame.draw.rect(screen, (0, 200, 0), (slot_x + 5, slot_y + 45, bar_width, 5))
                        pygame.draw.rect(screen, white, (slot_x + 5, slot_y + 45, 40, 5), 1)

    pygame.display.flip()
    clock.tick(fps)

save_game_data({"prologue_seen": True, "player_position": (char_x, char_y), "inventory": inventory_slots})
pygame.quit()
