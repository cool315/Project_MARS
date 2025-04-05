import pygame # 1. pygame 선언
import keyboard
 
pygame.init() # 2. pygame 초기화
 
# 3. pygame에 사용되는 전역변수 선언
WHITE = (255,255,255)
size = [1000,600]
screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode((x,y),FULLSCREEN)
 
done= False
clock= pygame.time.Clock()

player = pygame.image.load('pics/gjtlan001.png')
player = pygame.transform.scale(player, (100, 100))
 
# 4. pygame 무한루프
def runGame():
    playerMove()

def playerMove(): 
    global done, player
    x = 25
    y = 25

    to_x = 0
    to_y = 0
 
    while not done:
        clock.tick(10)
        screen.fill(WHITE)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True

            if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    to_x -= 2
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    to_x += 2
                if event.key == pygame.K_UP or event.key == pygame.K_w: 
                    to_y -= 2
                if event.key == pygame.K_DOWN or event.key == pygame.K_s: 
                    to_y += 2  

            if event.type == pygame.KEYUP: # 키를 떼엇을때 멈춘다
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    to_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    to_y = 0
        y += to_y
        x += to_x

        screen.blit(player, (x, y))
        pygame.display.update()
 
runGame()
pygame.quit()
