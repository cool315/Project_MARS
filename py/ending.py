
import pygame
import cv2

from py.setting import Font, Color, resource_path

small_font = Font().small_font

WHITE = Color().white
BLACK = Color().black

class Ending:
    def __init__(self):
        pass

    def ending(self, screen, background):
        self.fade_out(screen, background)
        pygame.time.delay(1000)
        self.ending_vid(screen)
        pygame.time.delay(1000)
        self.ending_credit(screen)

    def ending_vid(self, screen):
        cap = cv2.VideoCapture(resource_path("")) #여기다 엔딩 영상
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

    def ending_credit(self, screen):
        credits = [
            "감독: 박시원",
            "기획: 박시원, 엄도현, 윤정환",
            "프로그래밍: 박시원",
            "오프닝 영상: 엄도현",
            "엔딩 영상: 엄도현",
            "자료 조사: 윤정환",
            "잡일: 윤정환",
            "총 그림 담당: 허시무",
            "---------------Graphics---------------",
            "돔 건물: 허시무",
            "우주선: 허시무",
            "화성 배경: 허시무",
            "플레이어: 허시무",
            "각종 아이콘: 허시무",
            "빌런: 허시무",
            "돌: 허시무",
            "온실: 엄도현",
            "우주선 내부: 엄도현",
            "돔 내부: 허시무",
            "컴퓨터 화면: 허시무",
            "침대: 윤정환",
            "모니터: 허시무",
            "아이템 이동 애니매이션: 허시무",
            "오프닝 메뉴: 허시무",
            "토마토: 허시무",
            "감자: 허시무",
            "깻잎: 엄도현",
            "시계: 윤정환",
            "가방: 엄도현",
            "게임종료 아이콘: 윤정환",
            "--------------programming--------------",
            "게임 시스템: 박시원",
            "플레이어 이동: 박시원",
            "인벤토리 시스템: 박시원",
            "건물 상호작용: 박시원",
            "건물 설치 시스템: 박시원",
            "게임 저장 & 불러오기: 박시원",
            "ui 시스템: 박시원",
            "스토리 시스템: 박시원",
            "오프닝 시스템: 박시원",
            "엔딩 시스템: 박시원",
            "------------Special Thanks------------",
            "아이템 전송기: 윤원섭",
            "프로그래밍 도움: 나지성",
            "프로그래밍 도움: Chat gpt",
            "-----------------출처-------------------",
            "폰트: NEO 둥근모",
            "",
            "",
            "",
            "Thank you for playing!"
        ]

        clock = pygame.time.Clock()

        # 초기 위치
        start_y = screen.get_height()
        base_scroll_speed = 1.5  # 기본 스피드

        # 텍스트 surface와 위치 계산
        text_surfaces = [small_font.render(line, True, WHITE) for line in credits]
        text_positions = [
            (screen.get_width() // 2 - surf.get_width() // 2, start_y + i * 60)
            for i, surf in enumerate(text_surfaces)
        ]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(BLACK)

            # 스페이스바를 누르고 있으면 속도 2배
            keys = pygame.key.get_pressed()
            scroll_speed = base_scroll_speed * (2 if keys[pygame.K_SPACE] else 1)

            # 위치 갱신 및 그리기
            for i in range(len(text_positions)):
                x, y = text_positions[i]
                y -= scroll_speed
                text_positions[i] = (x, y)
                screen.blit(text_surfaces[i], (x, y))

            pygame.display.update()
            clock.tick(60)

            # 다 올라가면 종료
            if text_positions[-1][1] < -50:
                pygame.time.wait(2000)
                running = False

    def fade_out(self, screen, background):
        clock = pygame.time.Clock()

        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))

        alpha = 0  # 시작 투명도
        fade_speed = 5  # 어두워지는 속도  

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(background, (0, 0))

            # 어둡게 만들기
            if alpha < 255:
                alpha += fade_speed
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
            else:
                # 완전히 어두워진 상태
                fade_surface.set_alpha(255)
                screen.blit(fade_surface, (0, 0))
                running = False

            pygame.display.update()
            clock.tick(60)