# IMPORTS
import pygame

# Creating class Background
class Background:
    def __init__(self, image_path, screen_size):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, screen_size)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))






