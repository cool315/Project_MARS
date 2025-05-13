import pygame

from py.setting import Font, Screen, Color

screen = Screen.screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height

font = Font.font

white = Color.white
black = Color.black

class Opening:
    def __init__(self):
        self.captions = [
            ("나는 스페이스Z의 말단 회사원이였다.", 1),
            ("인턴으로 일한지 벌써 12년째", 1),
            ("드디어 나의 승진이 걸린 임무를 받았다.", 1),
            ("화성으로 가라는 스페이스Z에 명령에 따라 ", 1),
            ("화성으로 가서 비밀 프로젝트를 시작해야한다.", 1),
            ("비밀 프로젝트는 바로 화성을 테라포밍하는 것", 1),
            ("얼른 프로젝트를 끝내고 지구로 귀환하자.", 1)
        ]
    
    def show_caption(self):
        for text, duration in self.captions:
            screen.fill(black)
            label = font.render(text, True, white)
            label_rect = label.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(label, label_rect)
            pygame.display.flip()
            pygame.time.delay(duration * 1000)

    def starting_menu(self):
        