import pygame

# 캐릭터 이미지
character_up_imgs = pygame.image.load("pics/players/gjtlan004.png")
character_down_imgs = pygame.image.load("pics/players/gjtlan001.png")
character_left_imgs = pygame.image.load("pics/players/gjtlan002.png")
character_right_imgs = pygame.image.load("pics/players/gjtlan003.png")

class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load("pics/players/gjtlan001.png")
        self.direction = "down"
        self.speed = 3
        self.x, self.y = (x, y)

    def handle_event(self, event):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = "left"
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x +=    self.speed
            self.direction = "right"
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -=    self.speed
            self.direction = "up"
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y +=    self.speed
            self.direction = "down"
            moving = True

        # 캐릭터 방향 이미지 선택
        if self.direction == "up":
            self.img = character_up_imgs
        elif self.direction == "down":
            self.img = character_down_imgs
        elif self.direction == "left":
            self.img = character_left_imgs
        else:
            self.img = character_right_imgs

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))