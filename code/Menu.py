# IMPORTS
import pygame.image
from pygame import Surface, Rect, font
from pygame.font import Font

from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION, COLOR_WHITE, COLOR_PRIMARY, COLOR_GOLD, COLOR_SILVER, \
    COLOR_BRONZE
from code.Score import Score

# Creating class Menu
class Menu:
    def __init__(self, window):
        self.window = window
        self.bg = Background("./asset/MenuBg.png", (WIN_WIDTH, WIN_HEIGHT))
        self.score_handler = Score()
        self._menu_music_started = False
        self.start_menu_music()  # Inicia a música ao criar o menu

    def start_menu_music(self):
        if not pygame.mixer_music.get_busy():
            pygame.mixer_music.stop()
            pygame.mixer_music.load('./asset/Menu.mp3')
            pygame.mixer_music.play(-1)
            self._menu_music_started = True

    def run(self):
        menu_option = 0
        if not pygame.mixer_music.get_busy():
            self.start_menu_music()

        while True:
            # Drawing background
            self.bg.draw(self.window)

            # Title
            self.menu_text(80, "Dodger Cat", COLOR_PRIMARY, ((WIN_WIDTH / 2), 70), "Elephant")

            # Menu options
            for i in range(len(MENU_OPTION)):
                color = COLOR_WHITE if i == menu_option else COLOR_PRIMARY
                self.menu_text(30, MENU_OPTION[i], color, ((WIN_WIDTH / 2), 200 + 45 * i), "Arial Black")

            pygame.display.flip()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    if event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]


    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple, text_font:str):
        text_font: Font = pygame.font.SysFont(text_font, size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)

    # Creating a screen with the top 10 scores
    def show_top_scores(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)
            self.bg.draw(self.window)

            # Title
            self.menu_text(50, "TOP 10 SCORES", COLOR_PRIMARY, (WIN_WIDTH // 2, 50), "Elephant")

            # Score list
            top_scores = self.score_handler.get_scores()
            for idx, score in enumerate(top_scores):
                if idx == 0:
                    color = COLOR_GOLD
                elif idx == 1:
                    color = COLOR_SILVER
                elif idx == 2:
                    color = COLOR_BRONZE
                else:
                    color = COLOR_PRIMARY

                if idx < 5:
                    x_pos = WIN_WIDTH // 2 - 100
                    y_pos = 120 + idx * 35
                else:
                    x_pos = WIN_WIDTH // 2 + 100
                    y_pos = 120 + (idx - 5) * 35

                self.menu_text(30, f"{idx + 1}º : {score}", color, (x_pos, y_pos), "Arial Black")

            # Quit score menu
            self.menu_text(20, "Press ESC to back", COLOR_PRIMARY, (WIN_WIDTH // 2, WIN_HEIGHT - 40), "Arial Black")

            pygame.display.flip()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

    # Creating a screen with the controls
    def show_controls(self):
        clock = pygame.time.Clock()
        running = True

        cat_img = pygame.image.load('./asset/Cat.png')  # Substitua pelo caminho correto da imagem do gato
        cat_img = pygame.transform.scale(cat_img, (150, 150))  # Ajuste o tamanho conforme necessário
        cat_rect = cat_img.get_rect(center=(WIN_WIDTH // 2 + 200, WIN_HEIGHT // 2))

        while running:
            clock.tick(60)
            self.bg.draw(self.window)

            # Title
            self.menu_text(50, "HOW TO PLAY", COLOR_PRIMARY, (WIN_WIDTH // 2, 50), "Elephant")

            instructions = [
                "Use the left and right arrows",
                "to move the cat.",
                "Avoid the obstacles",
                "to score points!"
            ]

            start_y = 150
            for line in instructions:
                self.menu_text(20, line, COLOR_PRIMARY, (WIN_WIDTH // 2 - 200, start_y), "Arial Black")
                start_y += 40

            self.window.blit(cat_img, cat_rect)

            # Quit control menu
            self.menu_text(20, "Press ESC to back", COLOR_PRIMARY, (WIN_WIDTH // 2, WIN_HEIGHT - 40), "Arial Black")

            pygame.display.flip()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
