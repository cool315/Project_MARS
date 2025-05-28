import pygame

from py.player import Player
from py.opening import Opening
from py.UI import UI
from py.setting import Color, Screen, clock, Font, Save
from py.chat import StoryManager
from py.bulidings import spaceShip

#초기 설정
pygame.init()
pygame.display.set_caption("프로젝트 MARS")
screen = Screen.screen
screen_width, screen_height = (Screen.screen_width, Screen.screen_height)

player = Player(screen_width // 2 - 300, screen_height // 2 - 300)#플레이어
ui = UI()
spaceship = spaceShip()
story = StoryManager()
save = Save()

# 저장 파일 경로
SAVE_FILE = save.SAVE_FILE

if not save.IsSAVE_FILE:
    Opening().show_opening()
else:
    Opening().show_caption()
    Opening().starting_menu()

# 배경
background = pygame.image.load("pics/backgrounds/marsBackground1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        ui.handle_event(event)

    player.update(block_rects=[spaceship.image_rect])
    ui.update()
    spaceship.update()

    #화면 그리기
    screen.blit(background, (0, 0))

    player.render(screen)
    spaceship.render()
    ui.render()

    pygame.display.flip()
    clock.tick(60)

    if not save.IsSAVE_FILE:
        story.chat_render(1)
        save.create_game_data()
    
        

pygame.quit()