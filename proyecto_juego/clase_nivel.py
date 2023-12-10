
import pygame as pg
from constantes import abrir_config  
from clase_jugador import Jugador 

class Nivel:
    def __init__(self, screen: pg.surface.Surface, width, height, nombre_lvl):
        self.nombre_nivel = nombre_lvl  
    #     self.configuraciones = abrir_config().get(nombre_lvl)
    #     self.configuraciones_jugador = self.configuraciones.get('jugador')
    #     self.jugador_sprite = Jugador(coord_x=0, coord_y=0,  velocidad_caminar=20)
    #     self.music_path = self.configuraciones['nivel']['musica_fondo']
    #     self.sonido_disparo = self.configuraciones['nivel']['sonido_disparo']
    #     self.sonido_salto = self.configuraciones['nivel']['sonido_salto']
    

    
    # def cargar_music(self):

    #     nivel_config = self.configuraciones.get('nivel')
    #     self.music_path = nivel_config.get('musica_fondo', None)

    #     if self.music_path:
            
    #         pg.mixer.music.load(self.music_path)
    #         pg.mixer.music.set_volume(0.10)
    
    # def correr_musica(self):
    #     if self.music_path:
    #         pg.mixer.music.play(-1)  

    # def parar_musica(self):
    #     pg.mixer.music.stop()

