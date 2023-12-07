

import pygame 
from constantes import ANCHO_VENTANA    


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direccion = str):
        super().__init__()
        
        self.image = pygame.image.load('./imagenes/img_proyectil/sombrero.png')
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.rect.centery = pos_y
        self.rect.centerx = pos_x
        self.direccion = direccion 
    
    def update(self):
        if self.direccion == "derecha":
            self.rect.x += 10
            if self.rect.x >= ANCHO_VENTANA + 100:
                self.kill()
        elif self.direccion == "izquierda":
            self.rect.x -= 10 
            if self.rect.x <= -100:
                self.kill()