# IMPORTS
from abc import ABC, abstractmethod
import pygame.image

# Creating class Entity
class Entity(ABC):
    def __init__(self, name: str, position: tuple, size: tuple = None):
        self.name = name
        self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()
        if size:
            self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect(center=position)

    @abstractmethod
    def move(self):
        pass

