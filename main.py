import pygame

from py.player import Player
from py.opening import Opening
from py.UI import UI
from py.setting import Color, Screen, clock, Font, Save
from py.chat import StoryManager
from py.bulidings import spaceShip, Dome

#초기 설정
pygame.init()
pygame.display.set_caption("프로젝트 MARS")
screen = Screen.screen
screen_width, screen_height = (Screen.screen_width, Screen.screen_height)

player = Player(screen_width // 2 - 300, screen_height // 2 - 300)#플레이어
spaceship = spaceShip()
dome = Dome()
story = StoryManager()
save = Save()

save_data = None

inventory = [
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None]
] #기본 인벤토리 텅 빈거

# 저장 파일 경로
SAVE_FILE = save.SAVE_FILE

if not save.IsSAVE_FILE:
    Opening().show_opening()
else:
    Opening().show_caption()
    satrtMenu = Opening().starting_menu()

    if satrtMenu == "exit":
        pygame.quit()
    elif satrtMenu == "start":
        save_data = save.load_game_data()
        inventory = save_data['inventory']

ui = UI(save_data)

# 배경
background = pygame.image.load("pics/backgrounds/marsBackground1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

running = True
while running:
    #화면 그리기
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        ui.handle_event(event, inventory)

    player.update(block_rects=[spaceship.image_rect])
    ui.update()
    spaceship.update()

    player.render(screen)
    spaceship.render()
    ui.render(inventory)

    pygame.display.flip()
    clock.tick(60)

    if not save.IsSAVE_FILE:
        story.play_story(1)
        save.create_game_data((player.x, player.y), {
            "sec": ui.sec, 
            "min": ui.min, 
            "hou": ui.hou, 
            "day": ui.day
            })
        save_data = save.load_game_data()
        inventory = save_data['inventory']

        

pygame.quit