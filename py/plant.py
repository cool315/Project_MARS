import pygame

from py.setting import Screen, Color, Font

screen = Screen().screen
screen_width, screen_height = Screen().screen_width, Screen().screen_height

class Plant:
    def __init__(self):
        self.ground = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]

        self.DryGroundimg = pygame.image.load("pics/alt.png")
        self.DryGroundimg = pygame.transform.scale(self.DryGroundimg, (screen_width // 15, screen_width // 15))

        self.WetGroundimg = pygame.image.load("pics/alt.png")
        self.WetGroundimg = pygame.transform.scale(self.DryGroundimg, (screen_width // 15, screen_width // 15))

        self.tile_size = self.DryGroundimg.get_width()

    def render(self):
        start_x = screen_width // 2 - self.tile_size * 2.3
        start_y = screen_height // 2 - self.tile_size
        cols = 5
        rows = 5

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * self.tile_size
                y = start_y + row * self.tile_size
                screen.blit(self.DryGroundimg, (x, y))