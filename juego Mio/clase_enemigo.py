
from clase_surface import SurfaceManager as sf
import pygame as pg
from constantes import ANCHO_VENTANA, DEBUG

class Enemy:
    def __init__(self, coord_x, coord_y, frame_rate=100, velocidad_caminar=2, velocidad_ataque=10, move_frame_rate=100):
        self.__walk_r = sf.get_surface_from_spritesheet('image/img_enemy/enemy_1/enem_caminar.png', 5, 1, flip=True)
        self.__walk_l = sf.get_surface_from_spritesheet('image/img_enemy/enemy_1/enem_caminar.png', 5, 1)
        self.__atacar_r = sf.get_surface_from_spritesheet('image/img_enemy/enemy_1/enem_atack.png', 4, 1, flip=True)
        self.__atacar_l = sf.get_surface_from_spritesheet('image/img_enemy/enemy_1/enem_atack.png', 4, 1)
        self.__initial_x = coord_x
        self.__initial_y = coord_y
        self.__rect = None 
        self.__velocidad_caminar = velocidad_caminar
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__is_looking_right = True
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_r
        self.__actual_img_animation = None  # Inicializamos la animación como None al principio
        self.__animacion_ataque = False
        self.__velocidad_ataque = velocidad_ataque
        self.__move_frame_rate = move_frame_rate
        self.__move_player_time = 0

        # Inicializamos el rectángulo y la animación aquí después de cargar las imágenes
        self.__rect = pg.Rect(self.__initial_x, self.__initial_y, 0, 0)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]

    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    def caminar(self):
        look_right = self.__is_looking_right
        self.__set_x_animations_preset(self.__velocidad_caminar if look_right else -self.__velocidad_caminar,
                                    self.__walk_r if look_right else self.__walk_l, look_r=look_right)

    def do_movement(self, delta_ms):
        self.__move_player_time += delta_ms
        if self.__move_player_time >= self.__move_frame_rate:
            self.__move_player_time = 0

            # Guardo la posición antes de aplicar cambios
            old_x = self.__rect.x
            old_y = self.__rect.y

            # Actualizo las coordenadas del rectángulo
            self.__rect.x += self.__move_x

            # Cambiar la direccion al caminar
            if not (0 <= self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width()):
                self.__rect.x = old_x
                self.__is_looking_right = not self.__is_looking_right  # Cambia dirección
                self.__actual_animation = self.__walk_r if self.__is_looking_right else self.__walk_l  

            if not (0 <= self.__rect.y < 300):
                self.__rect.y = old_y

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0

            if self.__animacion_ataque:
                if self.__initial_frame >= len(self.__actual_animation) - 1:
                    self.__animacion_ataque = False
                else:
                    self.__initial_frame += 1
            else:
                
                if self.__initial_frame < len(self.__actual_animation) - 1:
                    self.__initial_frame += 1
                else:
                    self.__initial_frame = 0

    def actualizar_estado(self, delta_ms):
        self.animacion_ataque()
        
        self.caminar()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)

    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'green', self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def verificar_colision(self, estructuras):
        for estructura in estructuras:
            if self.__rect.colliderect(estructura.get_rect()):
                print("Colisión detectada con una estructura.")
                return True
        return False

    def animacion_ataque(self):
        if not self.__animacion_ataque:
            self.__animacion_ataque = True
            self.__player_animation_time = 0  
            self.__initial_frame = 0  
            look_right = self.__is_looking_right
            self.__set_x_animations_preset(0, self.__atacar_r if look_right else self.__atacar_l, look_r=look_right)

