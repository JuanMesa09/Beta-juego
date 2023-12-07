

import pygame as pg 
from constantes import *
from clase_jugador import Jugador
from clase_estructuras import Estructura
from clase_nivel import Nivel
from clase_enemigo import Enemigo


class Game():

    def __init__(self) :
        super().__init__()
        

    def correr_nivel(self, nombre_nivel):

        pg.init()
        pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        
        titulo = pg.display.set_caption("El paseo de Luffy")

        juego = Nivel(pantalla, ANCHO_VENTANA, ALTO_VENTANA, nombre_nivel)
        #juego.cargar_musica()
        pg.mixer.music.load("sonidos/musica lvl.mp3")

        retardo = pg.time.Clock()
        

        fondo = pg.image.load('./imagenes/img_fondo/goku_house.png')
        fondo = pg.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        juego_ejecutandose = True
        
        luffy = Jugador(0,400, velocidad_caminar=10,  cuadros_por_segundo= 60)

        
        font = pg.font.Font(None, 36)
        tiempo_duracion_derrota = 4000
        
        estructura1 = Estructura(100, 100, 50, 50, r'./imagenes/img_plataformas/plataforma_1.png')
        estructura2 = Estructura(300, 100, 50, 50, r'./imagenes/img_plataformas/plataforma_1.png')

        enemigo = Enemigo((0, 350))

        self.tiempo_inicial = pg.time.get_ticks()//1000 
        self.duracion_game =  10

        while juego_ejecutandose:
            lista_eventos = []
            pg.mixer.music.play(-1) 
            delta_ms = retardo.tick(FPS)

            pg.time.delay(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    juego_ejecutandose = False
                    break
                    
                lista_eventos.append(event)

            #tiempo transcurrido
            tiempo_actual =  pg.time.get_ticks() // 1000
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicial
            tiempo_restante = max(0, self.duracion_game - tiempo_transcurrido)
            
            #if tiempo_transcurrido >= self.duracion_game:
                #pantalla.fill((0, 0, 0))
                #texto_derrota = font.render(f"Tiempo Terminado DERRORTA", True, (255,255,255))
                ##pantalla.blit(texto_derrota, (ANCHO_VENTANA // 1 - texto_derrota.get_width() // 1, ALTO_VENTANA // 1 - texto_derrota.get_height() // 1))
            #else: 
                #pg.quit()
            
            
            
            tiempo_juego = font.render(f"Tiempo Restante {tiempo_restante}", True, (0,0,0))
            

            
            pantalla.blit(fondo, fondo.get_rect())
            pantalla.blit(tiempo_juego,(ANCHO_VENTANA//2, 10))
            
            estructura1.draw(pantalla)
            estructura2.draw(pantalla)
            luffy.bala_grupo.draw(pantalla)
            
            luffy.draw(pantalla)
            enemigo.draw(pantalla)
            luffy.update(delta_ms, lista_eventos)
            luffy.gravedad_activa()
            luffy.bala_grupo.update()
            enemigo.update()
            pg.display.update()
            
        juego.parar_musica() 
    pg.quit()


