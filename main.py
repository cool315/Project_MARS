import pygame
import pygame.image

from PIL import Image, ImageSequence

from py.player import Player
from py.opening import Opening
from py.UI import UI
from py.setting import Color, Screen, clock, Font, Save
from py.chat import StoryManager
from py.bulidings import spaceShip, Dome
from py.background import backgroundElementControl
from py.inventory import inventoryManage

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

background = backgroundElementControl("outside")

inventoryM = inventoryManage()

black = Color.black
white = Color.white

# 저장 파일 경로
SAVE_FILE = save.SAVE_FILE

def load_data():
    save_data = save.load_game_data()
    inventoryM.inventory = save_data['inventory']
    (player.x, player.y) = save_data['playerPos']
    (player.sizeX, player.sizeY) = save_data['playerSize']
    dome.IsConstructed = save_data['IsDomeCons']
    (dome.x, dome.y) = save_data['DomePos']

    if save_data['background'] == "outside":
        background.outSide()
        spaceship.IsPlaced = True
    elif save_data['background'] == "dome":
        background.InsideDome()
        spaceship.IsPlaced = False

    dome.IsPlaced = False

    return(save_data)


if not save.IsSAVE_FILE:
    Opening().show_opening()
else:
    Opening().show_caption()
    satrtMenu = Opening().starting_menu()

    if satrtMenu == "exit":
        pygame.quit()
    elif satrtMenu == "start":
        save_data = load_data()

ui = UI(save_data, inventoryM)

running = True
while running:
    #화면 그리기
    background.render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                mouse_pos = pygame.mouse.get_pos()
                if spaceship.rect.collidepoint(mouse_pos): #우주선 들어가기
                    if background.backgroundName == "outside":
                        background.InsideSpaceShip()

                        player.x, player.y = screen_width // 2, screen_height // 7 * 5  # 우주선 내부 좌표
                        player.sizeX, player.sizeY = screen_width // 30, screen_width // 15  # 플레이어 크기 조정

                        spaceship.IsPlaced = False
                        dome.IsPlaced = False
                elif dome.rect.collidepoint(mouse_pos): #돔 들어가기
                    if background.backgroundName == "outside":
                        background.InsideDome()

                        player.x, player.y = screen_width // 10 * 9, screen_height // 2  # 돔 내부 좌표
                        player.sizeX, player.sizeY = screen_width // 30, screen_width // 15  # 플레이어 크기 조정

                        spaceship.IsPlaced = False
                        dome.IsPlaced = False
                elif background.bed_rect and background.bed_rect.collidepoint(mouse_pos): # 침대 상호작용
                    if background.is_inside_dome:
                        screen.fill(black) #화면 전환
                        pygame.display.flip()

                        data = {
                            "playerPos": (background.bed_x, background.bed_y - player.sizeY - 10),
                            "playerSize": (player.sizeX, player.sizeY),
                            "sec": 0,
                            "min": 0,
                            "hou": 7,
                            "day": ui.day + 1,
                            "inventory": inventoryM.inventory,
                            "background": "dome",
                            "IsDomeCons": dome.IsConstructed,
                            "DomePos": (dome.x, dome.y)
                        }
                        save.save_game_data(data)
                        pygame.time.wait(3000)
                        
                        save_data = load_data()
                        ui = UI(save_data, inventoryM)
                elif background.monitor_rect and background.monitor_rect.collidepoint(mouse_pos): # 모니터 상호작용
                    if background.is_inside_dome:
                        background.computer()
                        player.hidden = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ui.exit_button_rect.collidepoint(event.pos):
                running = False
        ui.handle_event(event, dome)

    if background.is_inside_spaceship:
        if player.y > screen_height // 4 * 3:
            player.x, player.y = screen_width // 2 - 300, screen_height // 2 - 300  # 바깥 좌표
            player.sizeX, player.sizeY = screen_width // 50, screen_width // 25

            background.outSide()

            spaceship.IsPlaced = True
            dome.IsPlaced = True
    elif background.is_inside_dome:
        if player.x > screen_width:
            player.x, player.y = screen_width // 2 - 300, screen_height // 2 - 300  # 바깥 좌표
            player.sizeX, player.sizeY = screen_width // 50, screen_width // 25

            background.outSide()

            spaceship.IsPlaced = True
            dome.IsPlaced = True

    background.update()
    player.update(screen_surface=screen, backgroundName=background.backgroundName)
    ui.update()
    spaceship.update()
    dome.update()

    player.render(screen)
    spaceship.render()
    dome.render()

    ui.render(background.backgroundName)

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
        save_data = load_data()
        ui = UI(save_data, inventoryM)

        

pygame.quit