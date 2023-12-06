
import pygame as pg 
from constantes import *
from clase_proyectil import Proyectil
from clase_sprite_sheet import SurfaceManager as sf

class Jugador():

    def __init__(self, posicion_x, posicion_y, velocidad_caminar, bala_grupo,cuadros_por_segundo):
        super().__init__()
        self.vidas = 3
        self.parado_derecha = sf.get_surface_from_spritesheet('./imagenes/img_jugador/standar/paradito_derecha_1.png', 1, 7)
        self.parado_izquierda = sf.get_surface_from_spritesheet('./imagenes/img_jugador/standar/paradito_derecha_1.png', 1, 7, flip=True)
        self.correr_derecha = sf.get_surface_from_spritesheet('./imagenes/img_jugador/andar/correr_derecha.png', 1, 8)
        self.correr_izquierda = sf.get_surface_from_spritesheet('./imagenes/img_jugador/andar/correr_derecha.png', 1, 8, flip= True)
        self.suelo = ALTO_VENTANA
        self.gravedad = 1
        self.inicio = self.parado_derecha
        self.marco_inicial = 0
        self.actual_animacion = self.parado_derecha
        self.actual_animacion_imagen = self.actual_animacion[self.marco_inicial]
        self.rect = self.actual_animacion_imagen.get_rect(midbottom= (200,200))
        self.en_el_aire = False
        self.vel_x = velocidad_caminar
        self.vel_y = 0
        self.rect.x = posicion_x
        self.rect.y = posicion_y
        self.vel_salto = 10
        self.cd_disparo = 7
        self.recorrido_sprite = 1
        self.mirando_derecha =  True
        self.velocidad_salto = 10
        self.velocidad_disparo = 10
        self.direccion = "derecha"
        self.cd_disparo = 0
        self.jugador_reinicio = 0
        self.bala_grupo = bala_grupo
        self.cuadros_por_segundo = cuadros_por_segundo
        self.jugador_tiempo_animacion = 0
        self.animacion_disparo = False
    
    def animaciones_enx_presstablecidas(self,movimiento_en_x,lista_animaciones:[pg.surface.Surface], bandera_mirando_derecha):
        self.vel_x = movimiento_en_x
        self.actual_animacion = lista_animaciones
        self.mirando_derecha = bandera_mirando_derecha
        
    def caminar(self, direccion):
        

        if self.direccion == "derecha":
            mirando_derecha = True
            self.animaciones_enx_presstablecidas(self.vel_x, self.correr_derecha, bandera_mirando_derecha=mirando_derecha)

            
        elif self.direccion == "izquierda":
            mirando_derecha = False
            self.animaciones_enx_presstablecidas(-self.vel_x, self.correr_izquierda, bandera_mirando_derecha= mirando_derecha)

    def salto(self):

        if not self.en_el_aire:
            self.velocidad_y = self.velocidad_salto
            self.en_el_aire = True

    def gravedad_activa(self):
        if self.en_el_aire:
            self.rect.y = self.vel_y
            self.vel_y += self.gravedad
            #suelo
            if self.rect.y >= self.suelo:
                self.rect.y -= self.suelo
                self.en_el_aire = False
                self.vel_y -= 0
    

    def update(self, fotogramas_x_segundo):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.gravedad_activa()
        self.actualizar_cd()
        self.hacer_animacion(fotogramas_x_segundo)
    

    def crear_proyectil(self):
        if self.cd_disparo == 0:
            if self.mirando_derecha:
                proyectil = Proyectil(self.rect.centerx, self.rect.centery, "derecha")
            elif not self.mirando_derecha:
                proyectil = Proyectil(self.rect.centerx, self.rect.centery, "izquierda")
            
            self.cd_disparo = 10
            return proyectil
        else:
            return None

    def perdida_de_vidas(self):
        self.vidas -= 1
        if self.vidas <= 0:
            print("GAME OVER")
        
    def choque_enemigo(self):
        
        self.perder_vidas()
    

        
    def actualizar_cd(self):

        if self.cd_disparo > 0:
            self.cd_disparo -= 1


        
    # def draw(self, pantalla: pg.surface.Surface):

    #     if DEBUG:
    #         pg.draw.rect(pantalla, 'red', self.rect)
        
    def draw(self, pantalla: pg.surface.Surface):
        pantalla.blit(self.actual_animacion_imagen, self.rect)

    def hacer_animacion(self, fotograma_x_seg):
        self.jugador_tiempo_animacion += fotograma_x_seg
        if self.jugador_tiempo_animacion >= self.cuadros_por_segundo:
            self.jugador_tiempo_animacion = 0
            

            if self.animacion_disparo:
                
                if self.marco_inicial >= len(self.actual_animacion) - 1:
                    self.animacion_disparo = False
                    
                else:
                    self.marco_inicial += 1
                    
            else:
                
                # Lógica de animación normal
                if self.marco_inicial < len(self.actual_animacion) - 1:
                    self.marco_inicial += 1
                    
                else:
                    self.marco_inicial = 0
