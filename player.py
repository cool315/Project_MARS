import pygame

class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load("pics/players/gjtlan001.png")
        self.speed = 3
        self.x, self.y = (x, y)

    def handle_event(self, event):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            direction = "left"
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x +=    self.speed
            direction = "right"
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -=    self.speed
            direction = "up"
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y +=    self.speed
            direction = "down"
            moving = True

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))