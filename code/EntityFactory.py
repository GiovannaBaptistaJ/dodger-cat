# IMPORTS
from code.Cat import Cat
from code.Rock import Rock

# Creating class EntityFactory
class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, image_path, position):
        if entity_name.lower() == "cat":
            return Cat(image_path, position)
        elif entity_name.lower() == "rock":
            return Rock(image_path, position)
        else:
            return None


