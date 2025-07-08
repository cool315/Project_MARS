import pygame
from py.setting import Screen, resource_path

screen_width, screen_height = (Screen.screen_width, Screen.screen_height)

class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load(resource_path("pics/players/elon210.png"))

        self.IsHelmet = 2 # 2= ture, 1= false
        self.direction = 1 # 1= 정면, 2=왼쪽, 3=오른쪽, 4=후면
        self.movingNum = 0

        self.moving = 0
        self.speed = 3
        self.x, self.y = (x, y)
        self.sizeX, self.sizeY = (screen_width // 50, screen_width // 25)  # 플레이어 크기
        self.hidden = False #컴퓨터 등 특수상황에서 플레이어 숨기기

    def update(self, screen_surface=None, backgroundName=""):
        if not self.hidden:
            keys = pygame.key.get_pressed()
            old_x, old_y = self.x, self.y

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

            # 충돌 영역 체크
            if screen_surface:
                player_rect = pygame.Rect(self.x, self.y, self.sizeX, self.sizeY)
                hit_black = False

                # 여러 점 검사 (좌상, 우상, 좌하, 우하, 중심)
                points = [
                    player_rect.topleft,
                    player_rect.topright,
                    player_rect.bottomleft,
                    player_rect.bottomright,
                    player_rect.center,
                ]

                for px, py in points:
                    if 0 <= px < screen_surface.get_width() and 0 <= py < screen_surface.get_height():
                        color = screen_surface.get_at((px, py))
                        if color[:3] == (0, 0, 0):  # 검정
                            hit_black = True
                            break

                if hit_black:
                    self.x, self.y = old_x, old_y  # 이동 취소


            if(backgroundName == "outside"):
                self.IsHelmet = 2
            else:
                self.IsHelmet = 1

            self.movingNum = (self.moving // self.speed)
            if(self.movingNum >= 3):
                self.moving = 0


    def render(self, screen):
        if not self.hidden:
            if(self.movingNum == 0 or self.movingNum == 2):
                self.movingNum = 0
            elif(self.movingNum == 1):
                self.movingNum = 1
            else:
                if(self.direction == 2 or self.direction == 3):
                    self.movingNum = 1
                else:
                    self.movingNum = 2

            self.img = pygame.image.load(resource_path(f"pics/players/elon{self.IsHelmet}{self.direction}{self.movingNum}.png"))
            self.img = pygame.transform.scale(self.img, (self.sizeX, self.sizeY))

            screen.blit(self.img, (self.x, self.y))