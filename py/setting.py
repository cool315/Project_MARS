import pygame
import os
import json
import sys

pygame.init()

clock = pygame.time.Clock()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Screen:
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    fps = 60

class Color:
    white = (255, 255, 255)
    black = (1, 1, 1)
    gray = (180, 180, 180)
    dark_gray = (80, 80, 80)
    red = (255, 0, 0)

class Font:
    font_path = resource_path("font/neodgm.ttf")
    font = pygame.font.Font(font_path, int(Screen.screen_width // 23))
    small_font = pygame.font.Font(font_path, int(Screen.screen_width // 47))
    item_font = pygame.font.Font(font_path, int(Screen.screen_width // 120))

class Save:
    # 저장 파일 경로
    SAVE_FILE = resource_path("save/save_file.json")
    IsSAVE_FILE = os.path.exists(SAVE_FILE)

    def load_game_data(self):
        with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
        
    def create_game_data(self, player_position, Clock):
        self.basic_game_data = {
            "playerPos": player_position,
            "playerSize": (Screen.screen_width // 50, Screen.screen_width // 25),
            "playerSpeed": 3,
            "sec": Clock["sec"],
            "min": Clock["min"],
            "hou": Clock["hou"],
            "day": Clock["day"],
            "inventory": [
                    [{
                        "name": "돔 설치 도구",
                        "image": "pics/UI/items/DomeItem.png",
                        "placeimage": "pics/buildings/domeBuilding1.png",
                        "IsBuilding": True,
                        "IsSeed": False,
                        "IsFood": False,
                        "foodValue": None,
                        "placeType": "dome",
                        "description": "돔 설치 도구\n\n돔을 건설할 수 있는 아이템입니다.\n원하는 위치에 클릭하여 기지를 건설하세요.",
                        "count": 1
                    }, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None, None]
                ],
            "background": "outside",
            "IsDomeCons": False,
            "DomePos": (0, 0),
            "greenHouse": [
                [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
                [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
                [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
                [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
                [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
            ]
        }
        with open("save/save_file.json", "w", encoding="utf-8") as f:
            json.dump(self.basic_game_data, f, indent=4)
        self.IsSAVE_FILE = True

    def save_game_data(self, data):
        with open("save/save_file.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)