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
dome = Dome(0, 0, False)
story = StoryManager()
save = Save()

save_data = None

# 배경
background = pygame.image.load("pics/backgrounds/marsBackground1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

backgroundName = "outside"
is_inside_spaceship = False
is_inside_dome = False

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

running = True
while running:
    #화면 그리기
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_e:
                mouse_pos = pygame.mouse.get_pos()
                if spaceship.rect.collidepoint(mouse_pos):
                    is_inside_spaceship = not is_inside_spaceship  # 토글
                    if is_inside_spaceship:
                        background = pygame.image.load("pics/backgrounds/SpaceShipInside.png")
                        player.x, player.y = screen_width // 2, screen_height // 5 * 4  # 우주선 내부 좌표
                        player.sizeX, player.sizeY = screen_width // 30, screen_width // 15  # 플레이어 크기 조정
                        backgroundName = "SpaceshipInside"
                    else:
                        background = pygame.image.load("pics/backgrounds/marsBackground1.png")
                        player.x, player.y = screen_width // 2 - 300, screen_height // 2 - 300  # 바깥 좌표
                        player.sizeX, player.sizeY = screen_width // 50, screen_width // 25
                        backgroundName = "outside"
                elif dome.rect.collidepoint(mouse_pos):
                    is_inside_dome = not is_inside_dome
                    if is_inside_dome:
                        background = pygame.image.load("pics/backgrounds/DomeInside.png")
                        player.x, player.y = (screen_width // 2 - player.sizeX) , screen_height // 2
                        player.sizeX, player.sizeY = screen_width // 30, screen_width // 15
                        backgroundName = "DomeInside"
                    else:
                        background = pygame.image.load("pics/backgrounds/marsBackground1.png")
                        player.x, player.y = screen_width // 2 - 300, screen_height // 2 - 300  # 바깥 좌표
                        player.sizeX, player.sizeY = screen_width // 50, screen_width // 25
                        backgroundName = "outside"

                # 배경 크기 조정
                background = pygame.transform.scale(background, (screen_width, screen_height))

        ui.handle_event(event, inventory)

    player.update(block_rects=[spaceship.rect], backgroundName=backgroundName)
    ui.update()
    spaceship.update()

    player.render(screen)
    spaceship.render()
    dome.x = ui.domeX
    dome.y = ui.domeY
    dome.IsPlaced = ui.IsDomePlaced
    dome.render()

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