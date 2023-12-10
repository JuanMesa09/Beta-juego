
import pygame as pg
from constantes import abrir_config  
from clase_jugador import Jugador 

class Nivel:
    def __init__(self, screen: pg.surface.Surface, width, height, nombre_lvl):
        self.nombre_nivel = nombre_lvl  
        self.configuraciones = abrir_config().get(nombre_lvl)
        #self.configuraciones_jugador = self.configuraciones.get('player')
        #self.jugador_sprite = Jugador(coord_x=0, coord_y=0,  velocidad_caminar=20)
        #self.__music_path = self.configuraciones['nivel']['musica_fondo'] 
        #self.cargar_music()

    
    # def cargar_music(self):

    #     nivel_config = self.configuraciones.get('nivel')
    #     self.__music_path = nivel_config.get('musica_fondo', None)

    #     if self.__music_path:
            
    #         pg.mixer.music.load(self.__music_path)
    #         pg.mixer.music.set_volume(0.10)
    
    # def correr_musica(self):
    #     if self.__music_path:
    #         pg.mixer.music.play(-1)  

    def parar_musica(self):
        pg.mixer.music.stop()

