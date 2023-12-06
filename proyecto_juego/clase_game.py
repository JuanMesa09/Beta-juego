

import pygame as pg 
from constantes import *
from clase_jugador import Jugador
from clase_estructuras import Estructura
from clase_nivel import Nivel
from clase_enemigo import Enemigo


class Game():

    def __init__(self) :
        super().__init__()
        self.timer = 50

    def correr_nivel(self, nombre_nivel):

        pg.init()
        pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        
        titulo = pg.display.set_caption("El paseo de Luffy")

        juego = Nivel(pantalla, ANCHO_VENTANA, ALTO_VENTANA, nombre_nivel)
        #juego.cargar_musica()
        pg.mixer.music.load("sonidos/musica lvl.mp3")

        retardo = pg.time.Clock()
        bala_grupo = pg.sprite.Group()

        fondo = pg.image.load('./imagenes/img_fondo/goku_house.png')
        fondo = pg.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        juego_ejecutandose = True
        
        luffy = Jugador(0,ALTO_VENTANA, velocidad_caminar=10, bala_grupo=bala_grupo, cuadros_por_segundo= 60)

        
        
        
        estructura1 = Estructura(100, 100, 50, 50, r'./imagenes/img_plataformas/plataforma_1.png')
        estructura2 = Estructura(300, 100, 50, 50, r'./imagenes/img_plataformas/plataforma_1.png')

        enemigo = Enemigo((100, 200))
        
        while juego_ejecutandose:
            pg.mixer.music.play(-1) 
            delta_ms = retardo.tick(FPS)

            pg.time.delay(30)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        luffy.salto()
                    elif event.key == pg.K_r:
                        print("piu piu")
                        # luffy.crear_proyectil()
                        # nueva_bala = luffy.crear_proyectil()
                if event.type == pg.QUIT:
                    juego_ejecutandose = False
                    break
            
            
            lista_teclas_presionadas = pg.key.get_pressed()
            if lista_teclas_presionadas[pg.K_d]:
                luffy.caminar('derecha')
            elif lista_teclas_presionadas[pg.K_a]:
                luffy.caminar('izquierda')
            if not lista_teclas_presionadas[pg.K_d] and not lista_teclas_presionadas[pg.K_a]:
                luffy.estatico()
            
            

            
            pantalla.blit(fondo, fondo.get_rect())
            estructura1.draw(pantalla)
            estructura2.draw(pantalla)
            bala_grupo.draw(pantalla)
            luffy.draw(pantalla)
            enemigo.draw(pantalla)
            luffy.update(delta_ms)
            bala_grupo.update()
            pg.display.update()
            
        juego.parar_musica() 
    pg.quit()


