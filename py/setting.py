import pygame
import os
import json

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

class Save:
    # 저장 파일 경로
    SAVE_FILE = "save/save_data.json"
    IsSAVE_FILE = os.path.exists(SAVE_FILE)

    def load_game_data(self):
        if not self.IsSAVE_FILE:
            return {
                
            }
        with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)