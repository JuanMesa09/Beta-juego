


from constantes import DEBUG
import pygame as pg

class Estructura(pg.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, image_path):
        super().__init__()

        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (ancho, alto))
        self.rect = pg.Rect(x, y, ancho,alto)


    def get_rect(self):
        return self.rect

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            screen.blit(self.image, self.rect)

