import pygame
import cv2
from py.setting import Font, Screen, Color, Save

screen = Screen.screen
screen_width = Screen.screen_width
screen_height = Screen.screen_height
screen_size = screen.get_size()

font = Font.font
small_font = Font.small_font

white = Color.white
black = Color.black

save = Save()

class Opening:
    def __init__(self):
        self.captions = [
            ("나는 스페이스Z의 말단 회사원이였다.", 3),
            ("인턴으로 일한지 벌써 12년째", 3),
            ("드디어 나의 승진이 걸린 임무를 받았다.", 3),
            ("화성으로 가라는 스페이스Z에 명령에 따라 ", 3),
            ("화성으로 가서 비밀 프로젝트를 시작해야한다.", 4),
            ("비밀 프로젝트는 바로 화성을 테라포밍하는 것", 4),
            ("얼른 프로젝트를 끝내고 지구로 귀환하자.", 3)
        ]

        self.background = pygame.image.load("pics/opening/startMenu.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.startButton = pygame.Rect(screen_width - screen_width // 6, screen_height // 8 * 7, screen_width // 6, screen_height // 8)

    def show_caption(self):
        for text, duration in self.captions:
            start_time = pygame.time.get_ticks()
            skipped = False

            while True:
                screen.fill(black)
                label = font.render(text, True, white)
                label_rect = label.get_rect(center=(screen_width / 2, screen_height / 2))
                screen.blit(label, label_rect)

                # "아무 키나 눌러 스킵" 메시지
                skip_msg = small_font.render("'space'를 눌러 넘기기", True, white)
                skip_rect = skip_msg.get_rect(center=(screen_width / 2, screen_height - 50))
                screen.blit(skip_msg, skip_rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return  # 창 닫기
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            skipped = True
                            break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        skipped = True
                        break

                if skipped:
                    break

                elapsed = pygame.time.get_ticks() - start_time
                if elapsed >= duration * 1000:
                    break


    def starting_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return("exit") 
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.startButton.collidepoint(event.pos):
                            return("start") 
                            running = False
            screen.blit(self.background, (0, 0))

            pygame.draw.rect(screen, black, self.startButton)
            button_text = font.render("START", True, white)
            text_rect = button_text.get_rect(center=self.startButton.center)
            screen.blit(button_text, text_rect)

            pygame.display.flip()

    def scale_frame_to_screen(self, frame): #영상 화면 비율에 조정
        screen_w, screen_h = screen_size
        frame_h, frame_w = frame.shape[:2]
        ratio = min(screen_w / frame_w, screen_h / frame_h)
        new_w = int(frame_w * ratio)
        new_h = int(frame_h * ratio)
        x = (screen_w - new_w) // 2
        y = (screen_h - new_h) // 2
        resized_frame = cv2.resize(frame, (new_w, new_h))
        return resized_frame, (x, y)

    def show_opening(self):
        cap = cv2.VideoCapture("") #여기다 인트로 영상
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 1 or fps > 60:
            fps = 30

        show_skip_hint = False
        skip_hint_timer = 0  # 마지막 키 입력 시간

        running = True
        while running and cap.isOpened():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    else:
                        # 아무 키나 눌렀을 때 skip 메시지 표시
                        show_skip_hint = True
                        skip_hint_timer = pygame.time.get_ticks()

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            scaled_frame, position = self.scale_frame_to_screen(frame)
            surface = pygame.image.frombuffer(scaled_frame.tobytes(), scaled_frame.shape[1::-1], 'RGB')

            screen.fill((0, 0, 0))
            screen.blit(surface, position)

            # "ESC를 눌러 스킵" 메시지 표시
            if show_skip_hint:
                elapsed = pygame.time.get_ticks() - skip_hint_timer
                if elapsed > 3000:
                    show_skip_hint = False
                else:
                    skip_text = small_font.render("'space'를 눌러 스킵", True, (255, 255, 255))
                    screen.blit(skip_text, (0, screen_height - 30))

            pygame.display.flip()
            self.clock.tick(fps)

        cap.release()
