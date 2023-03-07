import pygame

class ShapeImages:
    def __init__(self, pygame: pygame) -> None:
        self.pygame = pygame
        self.sprites: dict[str: []] = {}

    def add_image(self, id: str, img_path, rc: pygame.Rect):
        self.sprites.update({id: [rc, pygame.image.load(img_path)]})

