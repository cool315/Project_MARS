import pygame
import pygame.image

from PIL import Image, ImageSequence

from py.player import Player
from py.opening import Opening
from py.UI import UI
from py.setting import Color, Screen, clock, Font, Save, resource_path
from py.chat import StoryManager
from py.bulidings import spaceShip, Dome
from py.background import backgroundElementControl
from py.inventory import inventoryManage
from py.ending import Ending
from py.plant import Plant

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

opening = Opening()
ending = Ending()

plant = Plant()

# 저장 파일 경로
SAVE_FILE = save.SAVE_FILE

def load_data():
    save_data = save.load_game_data()

    inventoryM.inventory = save_data['inventory']

    (player.x, player.y) = save_data['playerPos']
    (player.sizeX, player.sizeY) = save_data['playerSize']
    player.speed = save_data['playerSpeed']

    dome.IsConstructed = save_data['IsDomeCons']
    (dome.x, dome.y) = save_data['DomePos']

    plant.ground = save_data['greenHouse']

    if save_data['background'] == "outside":
        background.outSide()
        spaceship.IsPlaced = True
    elif save_data['background'] == "dome":
        background.InsideDome()
        spaceship.IsPlaced = False

    if(save_data["day"] > 1):
        spaceship.img = pygame.image.load(resource_path("pics/buildings/SpaceShipDestroyed.png"))
        spaceship.img = pygame.transform.scale(spaceship.img, (screen_width // 10, screen_height // 4))
        spaceship.IsDestroyed = True

    dome.IsPlaced = False

    return(save_data)

if not save.IsSAVE_FILE:
    opening.show_opening()
else:
    opening.show_caption()
    satrtMenu = opening.starting_menu()

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
                    if background.backgroundName == "outside" and not spaceship.IsDestroyed:
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
                        player.speed = 10  # 돔 내부에서의 플레이어 속도

                        spaceship.IsPlaced = False
                        dome.IsPlaced = False
                elif background.bed_rect and background.bed_rect.collidepoint(mouse_pos): # 침대 상호작용
                    if background.is_inside_dome:
                        screen.fill(black) #화면 전환
                        pygame.display.flip()

                        ui.day = ui.day + 1

                        rows = 5
                        cols = 5
                        for row in range(rows):
                            for col in range(cols):
                                if plant.ground[row][col]["dirtStatus"] == "wet":
                                    if plant.ground[row][col].get("type"):
                                        plant.ground[row][col]["grow"] += 1
                                plant.ground[row][col]["dirtStatus"] = "dry"  # 모든 타일의 흙 상태를 마른 상태로 초기화

                        if(ui.day == 2):
                            story.play_story(2)
                            spaceship.img = pygame.image.load(resource_path("pics/buildings/SpaceShipDestroyed.png"))
                            spaceship.img = pygame.transform.scale(spaceship.img, (screen_width // 10, screen_height // 4))

                        data = {
                            "playerPos": (background.bed_x, background.bed_y - player.sizeY - 10),
                            "playerSize": (player.sizeX, player.sizeY),
                            "playerSpeed": player.speed,
                            "sec": 0,
                            "min": 0,
                            "hou": 7,
                            "day": ui.day,
                            "inventory": inventoryM.inventory,
                            "background": "dome",
                            "IsDomeCons": dome.IsConstructed,
                            "DomePos": (dome.x, dome.y),
                            "greenHouse": plant.ground
                        }
                        save.save_game_data(data)
                        pygame.time.wait(3000)
                        
                        save_data = load_data()
                        ui.save_data = save_data
                        ui.save_update()
                elif background.monitor_rect and background.monitor_rect.collidepoint(mouse_pos): # 모니터 상호작용
                    if background.is_inside_dome:
                        background.computer()
                        player.hidden = True
                elif background.backgroundName == "GreenHouse": #온실 땅 상호작용
                    if not plant.harvest(mouse_pos, inventoryM):
                        plant.watering_click(mouse_pos)

            elif event.key == pygame.K_DELETE:
                ending.ending(screen, background.background)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ui.exit_button_rect.collidepoint(event.pos):
                running = False
        ui.handle_event(event, dome, plant, background)

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
            player.speed = 3  # 바깥에서의 플레이어 속도

            background.outSide()

            spaceship.IsPlaced = True
            dome.IsPlaced = True
        elif player.x < 0:
            player.x, player.y = screen_width // 8* 6 - 10, screen_height // 5 * 3
            player.sizeX, player.sizeY = screen_width // 40, screen_width // 20
            player.speed = 5  # 온실 내부에서의 플레이어 속도

            background.insideGreenHouse()
    elif background.backgroundName == "GreenHouse":
        plant.render()
        
        if player.x > screen_width // 8 * 6:
            background.InsideDome()

            player.x, player.y = screen_width // 10, screen_height // 2  # 돔 내부 좌표
            player.sizeX, player.sizeY = screen_width // 30, screen_width // 15  # 플레이어 크기 조정
            player.speed = 10

            spaceship.IsPlaced = False
            dome.IsPlaced = False

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