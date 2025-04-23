import pygame
import sys
import json
import os

# 초기 설정
pygame.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("산타듀밸리")

clock = pygame.time.Clock()
fps = 60

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
gray = (100, 100, 100)

# 폰트 설정 (사용자 폰트 경로)
font_path = "font/neodgm.ttf"
font = pygame.font.Font(font_path, 60)
small_font = pygame.font.Font(font_path, 40)

# 저장 파일 경로
SAVE_FILE = "save/save_data.json"
default_position = (screen_width // 2, screen_height // 2)

# 자막 리스트
captions = [
    ("대충 배경설명", 2),
    ("대충 오프닝", 2),
    ("대충 시작한다는 내용", 3)
]

# 버튼 위치 정의
continue_btn = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 50, 300, 80)
restart_btn = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 70, 300, 80)

# 함수 정의들
def draw_button(text, rect, color, font):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, white)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def show_caption(text, duration):
    screen.fill(black)
    label = font.render(text, True, white)
    label_rect = label.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(label, label_rect)
    pygame.display.flip()
    pygame.time.delay(duration * 1000)

def load_game_data():
    if not os.path.exists(SAVE_FILE):
        return {}
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def reset_game_data():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

def has_seen_prologue(data):
    return data.get("prologue_seen", False)

def save_prologue_seen(data):
    data["prologue_seen"] = True
    save_game_data(data)

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

# 파일 불러오기
game_data = load_game_data()

choice = show_load_menu()
if choice == "restart":
    if show_warning_message():
        reset_game_data()
        game_data = {}
        save_game_data({"prologue_seen": False, "player_position": default_position})

        for caption, duration in captions:
            show_caption(caption, duration)
        save_prologue_seen(game_data)
        char_x, char_y = default_position
    else:
        pos = game_data.get("player_position", default_position)
        char_x, char_y = pos
elif choice == "continue":
    pos = game_data.get("player_position", default_position)
    char_x, char_y = pos

# 프롤로그 처음 보는 경우 실행
if not has_seen_prologue(game_data):
    for caption, duration in captions:
        show_caption(caption, duration)
    save_prologue_seen(game_data)

# 배경, 캐릭터 이미지 로딩 (예시용 사각형으로 대체)
background = pygame.image.load("pics/marsBackground1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

character_up_imgs = pygame.transform.scale(pygame.image.load(f"pics/gjtlan004.png"), (100, 100))
character_down_imgs = pygame.transform.scale(pygame.image.load(f"pics/gjtlan001.png"), (100, 100))
character_left_imgs = pygame.transform.scale(pygame.image.load(f"pics/gjtlan002.png"), (100, 100))
character_right_imgs = pygame.transform.scale(pygame.image.load(f"pics/gjtlan003.png"), (100, 100))
                        
direction = "down"  # 기본 방향

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        char_x -= char_speed
        direction = "left"
        moving = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        char_x += char_speed
        direction = "right"
        moving = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        char_y -= char_speed
        direction = "up"
        moving = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        char_y += char_speed
        direction = "down"
        moving = True

    if direction == "up":
        current_images = character_up_imgs
    elif direction == "down":
        current_images = character_down_imgs
    elif direction == "left":
        current_images = character_left_imgs
    else:
        current_images = character_right_imgs

    screen.blit(background, (0, 0))
    screen.blit(current_images, (char_x, char_y))
    pygame.display.flip()

    clock.tick(fps)

# 종료 시 저장
save_game_data({"prologue_seen": True, "player_position": (char_x, char_y)})
pygame.quit()
