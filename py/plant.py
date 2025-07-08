import pygame

from py.setting import Screen, Color, Font, resource_path

screen = Screen().screen
screen_width, screen_height = Screen().screen_width, Screen().screen_height

small_font = Font().small_font

black = Color().black

class Plant:
    def __init__(self):
        self.ground = [
            [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
            [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
            [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
            [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
            [{"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}, {"dirtStatus": "dry"}],
        ]

        self.tile_size = screen_width // 20
        self.tile_rects = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]

        self.DryGroundimg = pygame.image.load(resource_path("pics/alt.png"))
        self.DryGroundimg = pygame.transform.scale(self.DryGroundimg, (self.tile_size, self.tile_size))

        self.WetGroundimg = pygame.image.load(resource_path("pics/plant/tomato5.png"))
        self.WetGroundimg = pygame.transform.scale(self.WetGroundimg, (self.tile_size, self.tile_size))

        self.potato_images = [
            pygame.transform.scale(pygame.image.load(resource_path("pics/plant/potato1.png")), (self.tile_size, self.tile_size)),
            pygame.transform.scale(pygame.image.load(resource_path("pics/plant/potato2.png")), (self.tile_size, self.tile_size)),
            pygame.transform.scale(pygame.image.load(resource_path("pics/plant/potato3.png")), (self.tile_size, self.tile_size)),
            pygame.transform.scale(pygame.image.load(resource_path("pics/plant/potato4.png")), (self.tile_size, self.tile_size)),
        ]

    def render(self):
        start_x = screen_width // 2 - self.tile_size * 2.3
        start_y = screen_height // 2 - self.tile_size
        cols = 5
        rows = 5

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * self.tile_size
                y = start_y + row * self.tile_size
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                self.tile_rects[row][col] = rect

                if self.ground[row][col]["dirtStatus"] == "dry":
                    screen.blit(self.DryGroundimg, (x, y))
                elif self.ground[row][col]["dirtStatus"] == "wet":
                    screen.blit(self.WetGroundimg, (x, y))

                if self.ground[row][col].get("type"):
                    plant_data = self.ground[row][col]

                    if plant_data["type"] == "potato":
                        if plant_data["grow"] == 0:
                            plant_image = self.potato_images[0]
                        elif plant_data["grow"] == 1:
                            plant_image = self.potato_images[1]
                        elif plant_data["grow"] == 2:
                            plant_image = self.potato_images[2]
                        else:
                            plant_image = self.potato_images[3]
                            self.ground[row][col]["harvestable"] = True
                    
                    plant_image = pygame.transform.scale(plant_image, (self.tile_size, self.tile_size))
                    screen.blit(plant_image, (x, y))
        
        self.hover_text(pygame.mouse.get_pos())

    def planting_click(self, mouse_pos, plant_type):
        for row in range(5):
            for col in range(5):
                rect = self.tile_rects[row][col]
                if rect and rect.collidepoint(mouse_pos):
                    if "type" not in self.ground[row][col]:
                        self.ground[row][col] = {
                            "dirtStatus": self.ground[row][col]["dirtStatus"],
                            "type": plant_type,
                            "grow": 0,
                            "harvestable": False
                        }
                        return True
        return False
    
    def watering_click(self, mouse_pos):
        for row in range(5):
            for col in range(5):
                rect = self.tile_rects[row][col]
                if rect and rect.collidepoint(mouse_pos):
                    self.ground[row][col]["dirtStatus"] = "wet"
    
    def hover_text(self, mouse_pos):
        for row in range(5):
            for col in range(5):
                rect = self.tile_rects[row][col]
                if rect and rect.collidepoint(mouse_pos) and self.ground[row][col].get("harvestable") == True:
                    text_surface = small_font.render("E키를 눌러 수확하기", True, black)
                    screen.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] - 20))
                    break
                elif rect and rect.collidepoint(mouse_pos) and self.ground[row][col]["dirtStatus"] == "dry":
                    # 마우스가 해당 타일 위에 있다면 텍스트 출력
                    text_surface = small_font.render("E키를 눌러 물주기", True, black)
                    screen.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] - 20))
                    break

    def harvest(self, mouse_pos, inventoryM):
        for row in range(5):
            for col in range(5):
                rect = self.tile_rects[row][col]
                if rect and rect.collidepoint(mouse_pos):
                    if self.ground[row][col].get("harvestable"):
                        self.ground[row][col] = {"dirtStatus": "dry"}

                        for row_idx, row in enumerate(self.inventoryM.inventory):
                            for col_idx, item in enumerate(row):
                                if item and item.get("name") == target_name:
                                    print(f"찾음: 위치=({row_idx}, {col_idx}), 아이템={item}")
                        if self.inventoryM.inventory
                        inventoryM.inventory.append()
                        return True
        return False