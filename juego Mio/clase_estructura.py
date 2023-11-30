

import pygame as pg

class Estructura(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_rect(self):
        return self.rect

    def draw(self, screen):
        screen.blit(self.image, self.rect)
