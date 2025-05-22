import pygame

from py.setting import Font, Screen, Color

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

font = Font().font

white = Color().white
black = Color().black

class StoryManager:
    def chat_render(self, text, second):
        pygame.draw.rect(screen, black, (0, screen_height//2, screen_width, screen_height//2))

        label = font.render(text, True, white)
        label_rect = label.get_rect(pos=(0, screen_height//2))
        screen.blit(label, label_rect)
        pygame.display.flip()
        pygame.time.delay(second * 1000)