# IMPORTS
from code.Entity import Entity
import random
from code.Const import WIN_WIDTH, WIN_HEIGHT

# Creating class rock
class Rock(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed = random.randint(4, 10)
        self.hitbox = self.rect.inflate(-10, -10)

    def move(self):
        self.rect.y += self.speed
        self.hitbox.center = self.rect.center

        # If stones leave the screen, they reappear
        if self.rect.top > WIN_HEIGHT:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.randint(20, WIN_WIDTH - 20)
            self.speed = random.randint(4, 10)
            self.hitbox.center = self.rect.center
            if hasattr(self, 'scored'):
                delattr(self, 'scored')
