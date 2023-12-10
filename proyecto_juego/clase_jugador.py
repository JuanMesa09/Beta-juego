
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
        self.retorno = None
        self.sonido_disparo = pg.mixer.Sound(r"./sonidos\audio_disp.mp3")
        self.sonido_salto = pg.mixer.Sound(r"./sonidos\audio_salt.mp3")
        self.tiempo_invulnerable = 2000  #en mili seg
        self.invulnerable = False
        self.tiempo_invulnerable_actual = 0
    
    def animaciones_enx_presstablecidas(self,movimiento_en_x,lista_animaciones:[pg.surface.Surface], bandera_mirando_derecha):
        self.rect.x += movimiento_en_x
        self.actual_animacion = lista_animaciones
        self.mirando_derecha = bandera_mirando_derecha
        
    def caminar(self, direccion):
        
        match direccion:
            case "derecha":
                self.mirando_derecha = True
                self.animaciones_enx_presstablecidas(self.vel_x, self.correr_derecha, bandera_mirando_derecha=self.mirando_derecha)
                
            case "izquierda":
                self.mirando_derecha = False
                self.animaciones_enx_presstablecidas(-self.vel_x, self.correr_izquierda, bandera_mirando_derecha= self.mirando_derecha)

    def estatico(self):
        if self.actual_animacion != self.parado_izquierda and self.actual_animacion != self.parado_derecha:
            self.actual_animacion = self.parado_derecha if self.mirando_derecha else self.parado_izquierda
            self.cuadro_inicial = 0
            
    def salto(self, estructuras):
        if not self.en_el_aire:
            self.vel_y = -self.velocidad_salto
            self.en_el_aire = True
        elif self.verificar_colision(estructuras) :
            self.en_el_aire = False

    def gravedad_activa(self):
        if self.en_el_aire:
            self.rect.y += self.vel_y  * 5
            self.vel_y += self.gravedad 
            
            #suelo
            if self.rect.y >= self.suelo:
                self.rect.y = self.suelo
                self.en_el_aire = False
                self.vel_y = 0


    def update(self, delta_ms, lista_eventos, pantalla, estructuras):
        self.actualizar_cd()
        self.hacer_animacion(delta_ms)
        self.hacer_movimiento(delta_ms)
        self.teclas_presionadas(lista_eventos, estructuras)
        self.bala_grupo.draw(pantalla)
        self.bala_grupo.update()
        
        
        #print(f"lista animacion acutal:  {self.actual_animacion}  numero de frame{self.marco_inicial}"  )
    

    def crear_proyectil(self, direccion):
        
        
        if direccion == "derecha":
                
            print("disparo a la derecha")
            return Proyectil(self.rect.centerx, self.rect.centery, "derecha")
            
        elif direccion == "izquierda":
            print("disparo a la izquierda")
            return Proyectil(self.rect.centerx, self.rect.centery, "izquierda" )
            #self.cd_disparo = 10
        
        
    def animacion_disparo(self, direccion):
        self.animacion_disparo_activa = True
        self.cuadro_inicial = 0
        
        match direccion:
            case "derecha":
                
                self.animaciones_enx_presstablecidas(self.velocidad_disparo, self.parado_derecha, "derecha")
                print("miro a la derecha")
            case "izquierda":
                print("miro a la izquierda")
                self.animaciones_enx_presstablecidas(-self.velocidad_disparo, self.parado_izquierda, "izquierda")
                #print("miro a la izquierda")

    
    def perdida_de_vidas(self):
        if not self.invulnerable:
            self.vidas -= 1
            self.invulnerable = True
            self.tiempo_invulnerable_actual = pg.time.get_ticks()

        
    def choque_enemigo(self):
        
        self.perdida_de_vidas()
    

        
    def actualizar_cd(self):

        if self.cd_disparo > 0:
            self.cd_disparo -= 1
        
    def draw(self, pantalla: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(pantalla, 'red', self.rect)
        if 0 <= self.marco_inicial < len(self.actual_animacion):
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
            

    def teclas_presionadas(self, lista_eventos, estructuras):
        
        for event in lista_eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.salto(estructuras)
                    self.sonido_salto.set_volume(0.15)
                    self.sonido_salto.play()
                elif event.key == pg.K_r:
                    self.animacion_disparo("derecha" if self.mirando_derecha else "izquierda")             
                    nuevo_proyectil = self.crear_proyectil(self.direccion)
                    self.bala_grupo.add(nuevo_proyectil)
                    self.sonido_disparo.set_volume(0.15)
                    self.sonido_disparo.play()
        teclas = pg.key.get_pressed()
        if teclas[pg.K_d]:
            self.mirando_derecha = True
            self.caminar('derecha')
            self.direccion = "derecha"
        elif teclas[pg.K_a]:
            self.mirando_derecha = False
            self.caminar('izquierda')
            self.direccion = "izquierda"
            
        if not teclas[pg.K_d] and not teclas[pg.K_a]:
            self.estatico()

    def ajustar_a_plataforma(self, platform_rect):
            # Ajusta la posición y la velocidad vertical del jugador según la plataforma
            if self.rect.colliderect(platform_rect) and self.rect.y < platform_rect.y:
                self.rect.y = platform_rect.y - self.rect.height
                self.vel_y = 0
                #self.en_el_aire = False
            elif self.rect.colliderect(platform_rect) and self.rect.y > platform_rect.y:
                self.rect.y = platform_rect.y - self.rect.height
                self.vel_y = 0
                #self.en_el_aire = False
                
    def verificar_colision(self, estructuras):
            for estructura in estructuras:
                if self.rect.colliderect(estructura.get_rect()):
                    
                    return True
            return False
    def agarrar_vida(self):

        self.vidas += 1