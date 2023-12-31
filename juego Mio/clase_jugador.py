

from clase_surface import SurfaceManager as sf
import pygame as pg
from constantes import ANCHO_VENTANA, DEBUG
from clase_proyectil import Proyectil

class Jugador:

    def __init__(self, coord_x, coord_y, frame_rate=100, speed_walk=2, gravity=16, salto=32, velocidad_disparo= 10):
        self.__iddle_r = sf.get_surface_from_spritesheet('./image/img_jugador/standar/paradito_derecha_1.png', 7, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('./image/img_jugador/standar/paradito_derecha_1.png', 7, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet('./image/img_jugador/andar/correr_derecha.png', 8, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('./image/img_jugador/andar/correr_derecha.png', 8, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet('./image/img_jugador/saltar/salto.png', 6, 1)
        self.__jump_l = sf.get_surface_from_spritesheet('./image/img_jugador/saltar/salto.png', 6, 1, flip=True)
        self.__tirar_r = sf.get_surface_from_spritesheet('./image/img_jugador/ataques/player_ataque.png', 5, 1)
        self.__tirar_l = sf.get_surface_from_spritesheet('./image/img_jugador/ataques/player_ataque.png', 5, 1, flip= True)
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__velocidad_disparo = velocidad_disparo
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True
        self.__vertical_speed = 0
        self.__animacion_disparo = False
        self.__jumpCount = 0


    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r


    def caminar(self, direction: str = 'Right'):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)

    def estatico(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0

    

    def do_movement(self, delta_ms):
        self._Jugador__player_move_time += delta_ms
        if self._Jugador__player_move_time >= self._Jugador__frame_rate:
            self._Jugador__player_move_time = 0

            # Guardo la posición antes de aplicar cambios
            old_x = self._Jugador__rect.x
            old_y = self._Jugador__rect.y

            self._Jugador__rect.x += self._Jugador__move_x

            # Muevo el jugador en el eje y teniendo en cuenta la velocidad vertical
            self._Jugador__rect.y += self._Jugador__move_y

            # Parte relacionada con saltar
            self.jump() 

            # Verifico el límite inferior
            if self._Jugador__rect.y > 300:
                self._Jugador__rect.y = 300
                self._Jugador__is_jumping = False
                self._Jugador__jumpCount = 0
                self._Jugador__move_y = 0

            # Verifico si el jugador está completamente dentro de los límites
            if not (0 <= self._Jugador__rect.x < ANCHO_VENTANA - self._Jugador__actual_img_animation.get_width()):
                self._Jugador__rect.x = old_x

            if not (0 <= self._Jugador__rect.y < 300):
                self._Jugador__rect.y = old_y
                self._Jugador__is_jumping = False
                self._Jugador__jumpCount = 0
                self._Jugador__move_y = 0

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            

            if self.__animacion_disparo:
                
                if self.__initial_frame >= len(self.__actual_animation) - 1:
                    self.__animacion_disparo = False
                    self.estatico() 
                else:
                    self.__initial_frame += 1
                    
            else:
                
                # Lógica de animación normal
                if self.__initial_frame < len(self.__actual_animation) - 1:
                    self.__initial_frame += 1
                    
                else:
                    self.__initial_frame = 0



    def actualizar_estado(self, delta_ms):
        bullet_group =  pg.sprite.Group()
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            pass

        if keys[pg.K_LSHIFT]:
            self.animacion_disparo('Right' if self._Jugador__is_looking_right else 'Left')
            
        elif keys[pg.K_d] and not keys[pg.K_a]:
            self.caminar('Right')
        elif keys[pg.K_a] and not keys[pg.K_d]:
            self.caminar('Left')
        else:
            self.estatico()

        self.do_movement(delta_ms)
        self.do_animation(delta_ms)


    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def verificar_colision(self, estructuras):
        for estructura in estructuras:
            if self.__rect.colliderect(estructura.get_rect()):
                return True
        return False
    
    
    def ajustar_a_plataforma(self, platform_rect):
        # Ajusta la posición y la velocidad vertical del jugador según la plataforma
        if self.__rect.colliderect(platform_rect) and self.__rect.y < platform_rect.y:
            self.__rect.y = platform_rect.y - self.__rect.height
            self.__vertical_speed = 0
    
    def crear_proyectil(self):
        
        
        if self.__is_looking_right:
            return Proyectil(self.__rect.centerx, self.__rect.centery, "Rigth")
            
        
        if not self.__is_looking_right:
            return Proyectil(self.__rect.centerx, self.__rect.centery, "Left")
            
    def animacion_disparo(self, direccion: str):
        self.__animacion_disparo = True
        self.__player_animation_time = 0  # Reinicio el tiempo de animación
        self.__initial_frame = 0  # Reinicio el cuadro inicial

        match direccion:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__velocidad_disparo, self.__tirar_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__velocidad_disparo, self.__tirar_l, look_r=look_right)
    def jump(self):
        if not self.__is_jumping:
            self.__is_jumping = False

        if self.__jumpCount >= -10:
            self.__move_y = -self.__jumpCount * abs(self.__jumpCount) * 0.5
            self.__jumpCount -= 1
        else:
            self.__jumpCount = 10
            self.__is_jumping = False