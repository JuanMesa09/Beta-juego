
import pygame as pg 

from constantes import *

from clase_sprite_sheet import SurfaceManager as sf

class Enemigo(pg.sprite.Sprite):

    def __init__(self, coordenadas):
        super().__init__()
        self.camina_derecha = sf.get_surface_from_spritesheet('imagenes/img_enemy/enemy_1/enem_caminar_derecha.png', 5, 1)
        self.camina_izquierda = sf.get_surface_from_spritesheet('imagenes/img_enemy/enemy_1/enem_caminar_izquierda.png', 5, 1)
        self.image = self.camina_izquierda[0]
        self.images_izquierda = self.camina_izquierda
        self.images_derecha = self.camina_derecha
        self.images = self.images_izquierda
        self.rect = self.image.get_rect()
        self.rect.midbottom = coordenadas
        self.velocidad_mov = 3
        self.direccion = 1
        self.puntaje = 500
        self.animacion_velocidad = 0.1
        self.animacion_tiempo = 0.0
        self.image_index = 0

    def update(self):
        # Movimiento constante
        self.rect.x += self.velocidad_mov * self.direccion

        # Límites de movimiento
        if self.rect.right > ANCHO_VENTANA - 200:
            self.direccion = -1
            self.images = self.images_izquierda
        elif self.rect.left < 150:
            self.direccion = 1
            self.images = self.images_derecha

        self.animacion_tiempo += 1 / FPS
        if self.animacion_tiempo >= self.animacion_velocidad:
            self.animacion_tiempo = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def draw(self, pantalla: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(pantalla, 'green', self.rect)
        pantalla.blit(self.image, self.rect)