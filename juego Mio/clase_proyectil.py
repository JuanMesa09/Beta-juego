import pygame 
from constantes import ANCHO_VENTANA    


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direccion = str):
        super().__init__()
        
        self.image = pygame.image.load('./image/img_proyectil/sombrero.png')
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.rect.centery = pos_y
        self.rect.centerx = pos_x
        self.direccion = direccion 
    
    def update(self):


        if  self.direccion == "Rigth":
                
                self.rect.x += 10
                if self.rect.x >= ANCHO_VENTANA + 100:
                    self.kill()
                    
        elif  self.direccion =="Left":

                self.rect.x -= 10 
                if self.rect.x >= ANCHO_VENTANA - 100:
                    self.kill()
        
