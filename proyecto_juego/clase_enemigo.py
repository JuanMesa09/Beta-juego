
import pygame as pg 

from constantes import *

from clase_proyectil import Proyectil
from clase_sprite_sheet import SurfaceManager as sf

class Enemigo ():

    def __init__ (self, coordenadas):

        super().__init__()
        self.camina_derecha = sf.get_surface_from_spritesheet('imagenes/img_enemy/enemy_1/enem_caminar_derecha.png',5 ,1)
        self.camina_izquierda = sf.get_surface_from_spritesheet('imagenes/img_enemy/enemy_1/enem_caminar_izquierda.png',5 ,1)
        self.ataque = sf.get_surface_from_spritesheet('imagenes/img_enemy/enemy_1/enem_atack.png',4, 1)
        self.image = self.camina_derecha
        self.inicio = self.camina_derecha
        self.marco_inicial = 0
        self.actual_animacion = self.inicio[self.marco_inicial]
        self.rect = self.actual_animacion.get_rect()
        self.rect.midbottom = coordenadas
        self.velocidad_mov = 3
        self.direccion = 1
        self.puntaje = 1000


    def update(self):
        #mov constante
        self.rect.x += self.velocidad_mov * self.direccion

        #limites movimiento
        if self.rect.right > ANCHO_VENTANA - 200:
            
            self.direccion = -1
            self.image = self.camina_izquierda
        
        elif self.rect.left < 150:
            self.direccion = 1

            self.image = self.camina_derecha

    def draw(self, pantalla: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(pantalla, 'red', self.rect)
        self.actual_animacion = self.inicio[self.marco_inicial]
        pantalla.blit(self.actual_animacion, self.rect)