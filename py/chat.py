import pygame

from py.setting import Font, Screen, Color

screen = Screen().screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

small_font = Font().small_font

white = Color().white
black = Color().black

class StoryManager:
    def chat_render(self, text, second):
        pygame.draw.rect(screen, black, (0, screen_height//2, screen_width, screen_height//2))

        label = small_font.render(text, True, white)
        label_rect = label.get_rect(topleft=(screen_width//30, screen_height//2 + screen_height//25))
        screen.blit(label, label_rect)
        pygame.display.flip()
        pygame.time.delay(second * 1000)
    def play_story(self, story_number):
        if (story_number == 1):
            self.chat_render("드디어 화성에 도착했다" ,2)
            self.chat_render("먼저 가방에서 돔 설치 도구를 꺼내 돔을 건설하자" ,3)
            self.chat_render("돔을 건설 한 후 컴퓨터를 열어 본부에 연락을 취해야지" ,4)
        elif (story_number == 2):
            self.chat_render("이게 무슨 소리지?" ,2)
            self.chat_render("화성의 모래폭풍이라니" ,3)
            self.chat_render("제발 아무 일 없이 지나가기를.." ,3)