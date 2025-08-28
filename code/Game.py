# IMPORTS
import pygame
from code.Const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTION
from code.Level import Level
from code.Menu import Menu

LEVEL_MUSIC_STARTED = False
MENU_MUSIC_STARTED = False

# Creating class Game
class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.menu = Menu(self.window)  # cria apenas uma vez

    def run(self):
        while True:
            option = self.menu.run()  # sempre usa o mesmo objeto Menu

            if option == MENU_OPTION[0]:
                level = Level(self.window, 'MenuBg1')
                level.run()  # joga
            elif option == MENU_OPTION[1]:
                self.menu.show_controls()
            elif option == MENU_OPTION[2]:
                self.menu.show_top_scores()
            elif option == MENU_OPTION[3]:
                pygame.quit()
                quit()