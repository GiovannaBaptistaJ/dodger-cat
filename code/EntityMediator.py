# IMPORTS
from code.Cat import Cat
from code.Rock import Rock

# Creating class EntityMediator
class EntityMediator:
    def __init__(self, entities):
        self.entities = entities
        self.score = 0
        self.game_over = False

    def update(self):
        cat = None
        rocks = []

        for e in self.entities:
            if isinstance(e, Cat):
                cat = e
            elif isinstance(e, Rock):
                rocks.append(e)

        if not cat:
            return

        for rock in rocks:
            if rock.rect.bottom < 0:
                continue

            if cat.hitbox.colliderect(rock.hitbox):
                self.game_over = True

            # Adding points for each stone passed
            elif rock.rect.top > cat.rect.bottom and not hasattr(rock, 'scored'):
                self.score += 1
                rock.scored = True
