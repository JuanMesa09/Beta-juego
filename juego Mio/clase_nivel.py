

import pygame as pg
from constantes import abrir_config  
from clase_jugador import Jugador 

class Nivel:
    def __init__(self, screen: pg.surface.Surface, width, height, nombre_lvl):
        self.stage_name = nombre_lvl  
        self.__configs = abrir_config().get(nombre_lvl)
        self.__jugador_configs = self.__configs.get('player')
        self.__jugador_sprite = Jugador(coord_x=0, coord_y=0, frame_rate=70, speed_walk=20)
        self.__music_path = self.__configs['nivel']['musica_fondo']  # Corrección aquí
        self.__load_music()

    
    def __load_music(self):

        nivel_config = self.__configs.get('nivel')
        self.__music_path = nivel_config.get('musica_fondo', None)

        if self.__music_path:
            
            pg.mixer.music.load(self.__music_path)
            pg.mixer.music.set_volume(0.10)
    
    def play_music(self):
        if self.__music_path:
            pg.mixer.music.play(-1)  

    def stop_music(self):
        pg.mixer.music.stop()
