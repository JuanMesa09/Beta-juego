import pygame as pg


class Estructura:
    def __init__(self, x, y, width, height, image_path):
        self.__rect = pg.Rect(x, y, width, height)
        self.__image = pg.image.load(image_path)
        self.__image = pg.transform.scale(self.__image, (width, height))  # Escalamos la imagen según el tamaño proporcionado

    def get_rect(self):
        return self.__rect

    def draw(self, screen):
        screen.blit(self.__image, self.__rect)