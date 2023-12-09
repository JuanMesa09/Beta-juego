
import pygame as pg 

class Puntaje:

    def __init__(self):
        self.puntaje = 0

    
    def muerte_enemiga(self, puntuacion):
        self.puntaje += puntuacion
    
    def agarrar_item(self, puntuacion):
        self.puntaje += puntuacion

    def  obtener_puntaje(self):
        return self.puntaje

    def obtener_item_vida(self):

        self.vida +=  1
