# FILE: code/Level.py

import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Cat import Cat
from code.Const import COLOR_WHITE, WIN_HEIGHT, WIN_WIDTH, COLOR_RED, COLOR_PRIMARY
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Background import Background
from code.Rock import Rock
from code.Score import Score
from code.EntityMediator import EntityMediator

class Level:
    def __init__(self, window: Surface, name: str):
        self.window = window
        self.name = name
        self.entity_list: list[Entity] = []
        self.bg = Background("./asset/LevelBg.png", (WIN_WIDTH, WIN_HEIGHT))

        # Criar o gato
        cat = EntityFactory.get_entity("cat", "Cat", (WIN_WIDTH // 2, WIN_HEIGHT - 50))
        cat.surf = pygame.transform.scale(cat.surf, (40, 40))
        cat.rect = cat.surf.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
        cat.hitbox = cat.rect.copy()
        self.entity_list.append(cat)

        # Criar pedras
        self.rocks_count = 6
        for _ in range(self.rocks_count):
            rock_x = random.randint(20, WIN_WIDTH - 20)
            rock_y = random.randint(-800, -50)
            rock = EntityFactory.get_entity("rock", "Rock", (rock_x, rock_y))
            rock.surf = pygame.transform.scale(rock.surf, (40, 40))
            rock.rect = rock.surf.get_rect(center=(rock_x, rock_y))
            rock.hitbox = rock.rect.copy()
            rock.speed = random.randint(4, 10)
            self.entity_list.append(rock)

        self.score_handler = Score()
        self.mediator = EntityMediator(self.entity_list)

        # Flags de controle
        self._score_saved = False
        self._level_music_started = False
        self._game_over_music_started = False

    def run(self):
        clock = pygame.time.Clock()

        # Toca música do level apenas uma vez
        if not self._level_music_started:
            pygame.mixer_music.stop()
            pygame.mixer_music.load('./asset/Level.mp3')
            pygame.mixer_music.play(-1)
            self._level_music_started = True

        while True:
            clock.tick(60)
            self.bg.draw(self.window)

            if not self.mediator.game_over:
                # Reset flag de música de game over
                self._game_over_music_started = False

                # Desenhar entidades
                for ent in self.entity_list:
                    ent.move()
                    self.window.blit(ent.surf, ent.rect)
                    ent.hitbox = ent.rect.copy()

                    # Pedras caindo
                    if isinstance(ent, Rock):
                        if ent.rect.top > WIN_HEIGHT:
                            ent.rect.y = random.randint(-200, -50)
                            ent.rect.x = random.randint(20, WIN_WIDTH - 20)
                            ent.speed = random.randint(4, 10)
                            if hasattr(ent, "scored"):
                                delattr(ent, "scored")
                            ent.hitbox = ent.rect.copy()

                self.mediator.update()

            else:
                # Game over
                if not self._score_saved:
                    self.score_handler.add_score(self.mediator.score)
                    self._score_saved = True

                # Para a música do level quando o game over ocorre
                if self._level_music_started:
                    pygame.mixer_music.stop()
                    self._level_music_started = False

                # Toca música de game over apenas uma vez
                if not self._game_over_music_started:
                    gameover_sound = pygame.mixer.Sound('./asset/GameOver.wav')  # cria Sound
                    gameover_sound.play()  # toca independente da música do level/menu
                    self._game_over_music_started = True

                for ent in self.entity_list:
                    if isinstance(ent, Cat):
                        ent.update(self.window)
                        ent.die()
                        self.level_text_centered(50, "GAME OVER!", COLOR_RED, WIN_HEIGHT // 2 - 20)
                        self.level_text_centered(18, "Press ENTER to restart", COLOR_WHITE, WIN_HEIGHT // 2 + 20)
                    elif isinstance(ent, Rock):
                        self.window.blit(ent.surf, ent.rect)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    return "restart"

            # Mostrar score
            self.level_text(30, f"Score: {self.mediator.score}", COLOR_PRIMARY, (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self._score_saved:
                        self.score_handler.add_score(self.mediator.score)
                        self._score_saved = True
                    pygame.quit()
                    sys.exit()

            # Mostrar fps
            self.level_text(14, f"fps: {clock.get_fps():.0f}", COLOR_WHITE, (10, WIN_HEIGHT - 35))

            pygame.display.flip()

    # Funções de desenho de texto
    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font: Font = pygame.font.SysFont("Arial Black", size=text_size)
        surf: Surface = font.render(text, True, text_color).convert_alpha()
        rect: Rect = surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(surf, rect)

    def level_text_centered(self, text_size: int, text: str, text_color: tuple, y_pos: int):
        font: Font = pygame.font.SysFont("Arial Black", text_size)
        surf: Surface = font.render(text, True, text_color).convert_alpha()
        rect: Rect = surf.get_rect(center=(WIN_WIDTH // 2, y_pos))
        self.window.blit(surf, rect)
