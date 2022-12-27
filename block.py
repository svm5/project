import pygame


class BaseBlock(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, width, height):
        super().__init__()
        self.name = name
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    
class Grass(BaseBlock):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__("grass", pos_x, pos_y, width, height)


class Land(BaseBlock):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__("land", pos_x, pos_y, width, height)