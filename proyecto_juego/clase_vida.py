
import pygame as pg
from clase_jugador import Jugador 

class Vida(pg.sprite.Sprite):

    def __init__(self, panth_imagen, x, y, ancho, alto):

        super().__init__()

        self.image = pg.image.load(panth_imagen).convert_alpha()
        self.image = pg.transform.scale(self.image, (ancho, alto))
        self.rect = pg.Rect(x, y, ancho, alto)
        self.vidas = Jugador.self.vidas
    

    

    def draw(self, pantalla): 
        pantalla.blit(self.image, self.rect)
    

    def obtener_info_vida(self):
        
        return self.vidas

