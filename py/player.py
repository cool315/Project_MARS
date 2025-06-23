import pygame
from py.setting import Screen

screen_width, screen_height = (Screen.screen_width, Screen.screen_height)

class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load("pics/players/elon210.png")

        self.IsHelmet = 2 # 2= ture, 1= false
        self.direction = 1 # 1= 정면, 2=왼쪽, 3=오른쪽, 4=후면
        self.movingNum = 0

        self.moving = 0
        self.speed = 3
        self.x, self.y = (x, y)
        self.sizeX, self.sizeY = (screen_width // 50, screen_width // 25)  # 플레이어 크기

    def handle_event(self, event):
        pass

    def update(self, block_rects=None, backgroundName=""):
        if block_rects is None:
            block_rects = []

        keys = pygame.key.get_pressed()
        old_x, old_y = self.x, self.y  # 이전 위치 저장

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = 2
            self.moving += 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 3
            self.moving += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = 4
            self.moving += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.direction = 1
            self.moving += 1

        # 충돌 확인용 rect
        player_rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        for rect in block_rects:
            if player_rect.colliderect(rect):
                self.x, self.y = old_x, old_y  # 충돌 시 되돌림
                break

        if(backgroundName == "outside"):
            self.IsHelmet = 2
        else:
            self.IsHelmet = 1

        self.movingNum = (self.moving // self.speed)
        if(self.movingNum >= 3):
            self.moving = 0


    def render(self, screen):

        if(self.movingNum == 0 or self.movingNum == 2):
            self.movingNum = 0
        elif(self.movingNum == 1):
            self.movingNum = 1
        else:
            if(self.direction == 2 or self.direction == 3):
                self.movingNum = 1
            else:
                self.movingNum = 2

        self.img = pygame.image.load(f"pics/players/elon{self.IsHelmet}{self.direction}{self.movingNum}.png")
        self.img = pygame.transform.scale(self.img, (self.sizeX, self.sizeY))

        screen.blit(self.img, (self.x, self.y))