# FILE: code/Cat.py

# IMPORTS
import pygame
from code.Entity import Entity
from code.Const import WIN_WIDTH


class Cat(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed = 5
        self.alive = True
        self.hitbox = self.rect.inflate(-20, -20)

        # Frames de morte
        self.dead_frames = [
            pygame.image.load("./asset/05_Dead/__Cat_Dead_000.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_001.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_002.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_003.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_004.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_005.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_006.png"),
            pygame.image.load("./asset/05_Dead/__Cat_Dead_007.png"),
        ]
        self.dead_frames = [pygame.transform.scale(img, (64, 64)) for img in self.dead_frames]

        # Controle da animação de morte
        self.frame_index = 0
        self.frame_delay = 10
        self.frame_count = 0

        # Frames de caminhada
        self.walk_frames = [
            pygame.image.load("./asset/02_Run/__Cat_Run_000.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_001.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_002.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_003.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_004.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_005.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_006.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_007.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_008.png"),
            pygame.image.load("./asset/02_Run/__Cat_Run_009.png"),
        ]
        self.walk_frames = [pygame.transform.scale(img, (64, 64)) for img in self.walk_frames]

        # Inicializa com o primeiro frame
        self.image = self.walk_frames[0]

        # Controle da animação de caminhada
        self.current_frame = 0
        self.frame_delay_walk = 5
        self.frame_counter = 0

        # Som de caminhada (canal separado para não interromper música do level)
        self.walk_sound = pygame.mixer.Sound('./asset/WalkingCat.flac')
        self.walk_channel = pygame.mixer.Channel(1)

    def move(self):
        if not self.alive:
            return  # morto não se move

        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed
            moving = True

        # Atualiza a animação de caminhada
        if moving:
            if not self.walk_channel.get_busy():
                self.walk_channel.play(self.walk_sound)

            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay_walk:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame]
        else:
            # Quando parado, mostra o primeiro frame
            self.image = self.walk_frames[0]

        # Mantém a hitbox alinhada
        self.hitbox.center = self.rect.center

    def die(self):
        self.alive = False
        self.frame_index = 0
        self.frame_count = 0

    def update(self, window):
        if self.alive:
            window.blit(self.image, self.rect)
        else:
            # Animação de morte
            if self.frame_index < len(self.dead_frames):
                window.blit(self.dead_frames[self.frame_index], self.rect)
                self.frame_count += 1
                if self.frame_count >= self.frame_delay:
                    self.frame_count = 0
                    self.frame_index += 1
