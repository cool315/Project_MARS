import pygame

# 캐릭터 이미지
character_up_imgs = pygame.image.load("pics/players/elon004.png")
character_down_imgs = pygame.image.load("pics/players/elon001.png")
character_left_imgs = pygame.image.load("pics/players/elon002.png")
character_right_imgs = pygame.image.load("pics/players/elon003.png")

class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load("pics/players/elon001.png")
        self.direction = "down"
        self.speed = 3
        self.x, self.y = (x, y)

    def handle_event(self, event):
        pass

    def update(self, block_rects=None):
        if block_rects is None:
            block_rects = []

        keys = pygame.key.get_pressed()
        old_x, old_y = self.x, self.y  # 이전 위치 저장

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.direction = "down"

        # 충돌 확인용 rect
        player_rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        for rect in block_rects:
            if player_rect.colliderect(rect):
                self.x, self.y = old_x, old_y  # 충돌 시 되돌림
                break

        # 방향 이미지 적용
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