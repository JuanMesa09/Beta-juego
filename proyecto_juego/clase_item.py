

import pygame as pg 


class Item (pg.sprite.Sprite):
    def __init__(self, panth_imagen, x, y, ancho, alto):
        super().__init__()
        self.image = pg.image.load(panth_imagen).convert_alpha()
        self.image = pg.transform.scale(self.image, (ancho, alto))
        self.rect = pg.Rect(x, y, ancho, alto)
        self.puntaje = 100
        
    
    
    def get_rect(self):
        return self.rect
    
    def draw(self, pantalla): 
        pantalla.blit(self.image, self.rect)

