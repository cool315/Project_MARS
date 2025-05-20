import pygame

pygame.init()

clock = pygame.time.Clock()

class Screen:
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    fps = 60

class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (100, 100, 100)

class Font:
    font_path = "font/neodgm.ttf"
    font = pygame.font.Font(font_path, int(Screen.screen_width // 23))
    small_font = pygame.font.Font(font_path, 20)