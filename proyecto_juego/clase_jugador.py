
import pygame as pg 
from constantes import *
from clase_proyectil import Proyectil
from clase_sprite_sheet import SurfaceManager as sf

class Jugador():

    def __init__(self, posicion_x, posicion_y, velocidad_caminar,cuadros_por_segundo):
        super().__init__()
        self.vidas = 3
        self.parado_derecha = sf.get_surface_from_spritesheet('./imagenes/img_jugador/standar/paradito_derecha_1.png', 7, 1)
        self.parado_izquierda = sf.get_surface_from_spritesheet('./imagenes/img_jugador/standar/paradito_derecha_1.png', 7, 1, flip=True)
        self.correr_derecha = sf.get_surface_from_spritesheet('./imagenes/img_jugador/andar/correr_derecha.png', 8, 1)
        self.correr_izquierda = sf.get_surface_from_spritesheet('./imagenes/img_jugador/andar/correr_derecha.png', 8, 1, flip= True)
        self.suelo = ALTO_VENTANA
        self.gravedad = 3
        self.inicio = self.parado_derecha
        self.marco_inicial = 0
        self.actual_animacion = self.parado_derecha
        self.actual_animacion_imagen = self.actual_animacion[self.marco_inicial]
        self.rect = self.actual_animacion_imagen.get_rect(midbottom= (200,200))
        self.en_el_aire = False
        self.vel_x = velocidad_caminar
        self.vel_y = 10
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
        self.bala_grupo = pg.sprite.Group()
        self.cuadros_por_segundo = cuadros_por_segundo
        self.jugador_tiempo_animacion = 0
        self.animacion_disparo_activa = False
        self.tiempo_de_movimiento = 0
    
    def animaciones_enx_presstablecidas(self,movimiento_en_x,lista_animaciones:[pg.surface.Surface], bandera_mirando_derecha):
        self.rect.x += movimiento_en_x
        self.actual_animacion = lista_animaciones
        self.mirando_derecha = bandera_mirando_derecha
        
    def caminar(self, direccion):
        
        match direccion:
            case "derecha":
                mirando_derecha = True
                self.animaciones_enx_presstablecidas(self.vel_x, self.correr_derecha, bandera_mirando_derecha=mirando_derecha)
                
            case "izquierda":
                mirando_derecha = False
                self.animaciones_enx_presstablecidas(-self.vel_x, self.correr_izquierda, bandera_mirando_derecha= mirando_derecha)

    def estatico(self):
        if self.actual_animacion != self.parado_izquierda and self.actual_animacion != self.parado_derecha:
            self.actual_animacion = self.parado_derecha if self.mirando_derecha else self.parado_izquierda
            self.cuadro_inicial = 0
            
    def salto(self):
        if not self.en_el_aire:
            self.vel_y = -self.velocidad_salto
            self.en_el_aire = True

    def gravedad_activa(self):
        if self.en_el_aire:
            self.rect.y += self.vel_y  * 6
            self.vel_y += self.gravedad 
            
            #suelo
            if self.rect.y >= self.suelo:
                self.rect.y = self.suelo
                self.en_el_aire = False
                self.vel_y = 0


    def update(self, delta_ms, lista_eventos):
        self.actualizar_cd()
        self.hacer_animacion(delta_ms)
        self.hacer_movimiento(delta_ms)
        self.teclas_presionadas(lista_eventos)
        #print(f"lista animacion acutal:  {self.actual_animacion}  numero de frame{self.marco_inicial}"  )
    

    def crear_proyectil(self):
        if self.cd_disparo == 0:
            if self.mirando_derecha:
                return Proyectil(self.rect.centerx, self.rect.centery, "derecha")
            
            elif self.mirando_derecha:
                return Proyectil(self.rect.centerx, self.rect.centery, "izquierda")
            self.cd_disparo = 10
        
        
    def animacion_disparo(self, direccion):
        self.animacion_disparo_activa = True
        self.cuadro_inicial = 0
        mirando_derecha = self.mirando_derecha
        match direccion:
            case "derecha":
                
                self.animaciones_enx_presstablecidas(self.velocidad_disparo, self.parado_derecha, bandera_mirando_derecha= mirando_derecha)
            
            case "izquierda":
                
                self.animaciones_enx_presstablecidas(-self.velocidad_disparo, self.parado_izquierda, bandera_mirando_derecha= not mirando_derecha)
                
    
    def perdida_de_vidas(self):
        self.vidas -= 1
        if self.vidas <= 0:
            print("GAME OVER")
        
    def choque_enemigo(self):
        
        self.perdida_de_vidas()
    

        
    def actualizar_cd(self):

        if self.cd_disparo > 0:
            self.cd_disparo -= 1
        
    def draw(self, pantalla: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(pantalla, 'red', self.rect)
        self.actual_animacion_imagen = self.actual_animacion[self.marco_inicial]
        pantalla.blit(self.actual_animacion_imagen, self.rect)
        
    def hacer_animacion(self, delta_ms):

        self.jugador_tiempo_animacion += delta_ms
        if self.jugador_tiempo_animacion >= self.cuadros_por_segundo:
            self.jugador_tiempo_animacion = 0
            
            
            if self.marco_inicial < len(self.actual_animacion) - 1:
                self.marco_inicial += 1
                    
            else:
                self.marco_inicial = 0
        
        
    def hacer_movimiento(self,delta_ms):
        
        self.tiempo_de_movimiento += delta_ms
        if self.tiempo_de_movimiento >= self.marco_inicial:#self.cuadros_por_segundo:
            self.tiempo_de_movimiento = 0
            
        
            if self.rect.y > 300:
                self.rect.y = 300
                self.en_el_aire = False
                self.vel_y = 0
                
            #LIMITES para q no se salga
            if self.rect.left <= -1:
                self.rect.left = -1
            elif self.rect.right >= ANCHO_VENTANA + 1:
                self.rect.right = ANCHO_VENTANA + 1
            elif self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= ALTO_VENTANA + 1:
                self.rect.bottom = ALTO_VENTANA + 1
            

    def teclas_presionadas(self, lista_eventos):
        
        for event in lista_eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.salto()
                elif event.key == pg.K_r:
                    self.animacion_disparo("derecha" if self.mirando_derecha else "izquierda")             
                    nuevo_proyectil = self.crear_proyectil()
                    self.bala_grupo.add(nuevo_proyectil)
        teclas = pg.key.get_pressed()
        if teclas[pg.K_d]:
            self.caminar('derecha')
        elif teclas[pg.K_a]:
            self.caminar('izquierda')
                
        if not teclas[pg.K_d] and not teclas[pg.K_a]:
            self.estatico()



