

import random
import pygame as pg 
from constantes import *
from clase_jugador import Jugador
from clase_estructuras import Estructura
from clase_nivel import Nivel
from clase_enemigo import Enemigo
from clase_puntaje import Puntaje
from clase_item import Item

from clase_trampas import Trampa


class Game():

    def __init__(self) :
        super().__init__()
        

    def correr_nivel(self, nombre_nivel):

        self.icono_vida =pg.transform.scale(pg.image.load(r'./imagenes\vidas\vida_mate.png'), (25,25))
        self.rect = self.icono_vida.get_rect()
        
        pg.init()
        pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

        


        titulo = pg.display.set_caption("El paseo de Luffy")
        font = pg.font.Font(None, 36)
        juego = Nivel(pantalla, ANCHO_VENTANA, ALTO_VENTANA, nombre_nivel)
        
        
        retardo = pg.time.Clock()
        

        fondo = pg.image.load('./imagenes/img_fondo/imagen_fondo_nueva.png')
        fondo = pg.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        juego_ejecutandose = True
        NUMERO_ENEMIGOS = 2


        
        grupo_enemigos = pg.sprite.Group()
        grupo_trampas = pg.sprite.Group()
        grupo_items = pg.sprite.Group()
        
        
        


        item_puntaje_1 = Item(r'imagenes\img_items\item_puntos\puntajee.png',80 ,190, 40,40)
        item_vida_1 = Item(r'imagenes\vidas\vida_mate.png',370 ,190, 40,40)
        grupo_items.add(item_puntaje_1, item_vida_1)

        trampa_1 = Trampa(r'imagenes\trampas\pinches.png', 300,315 , 30, 30)

        grupo_trampas.add(trampa_1)
        


        
        for _ in range(NUMERO_ENEMIGOS):
            x =  random.randint(300, 500)
            y =  350
            enemigos = Enemigo((x,y))
            grupo_enemigos.add(enemigos)





        self.puntaje = Puntaje()

        self.luffy = Jugador(0,400, velocidad_caminar=5,  cuadros_por_segundo= 60)
        
        
        
        
        #tiempo_duracion_derrota = 4000
        
        estructura1 = Estructura(100, 200, 50, 50, r'./imagenes/img_plataformas/plataforma_1.png')
        estructura2 = Estructura(150, 200, 50, 50, r'./imagenes/img_plataformas/plataforma_1.png')
        estructura3 = Estructura(400, 200, 50, 50, r'./imagenes/img_plataformas/ladrillito.png')
        estructura4 = Estructura(450, 200, 50, 50, r'./imagenes/img_plataformas/ladrillito.png')

        lista_estructuras = [estructura1, estructura2, estructura3, estructura4]
        

        self.tiempo_inicial = pg.time.get_ticks()//1000 
        self.duracion_game =  40

        while juego_ejecutandose:
            lista_eventos = []
            
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
            
            if tiempo_transcurrido >= self.duracion_game:
                juego_ejecutandose =  False
                pantalla.fill((0, 0, 0))
                texto_victoria = font.render(f"Tiempo Terminado DERRORTA", True, (255,255,255))
                texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                pantalla.blit(texto_puntaje_victoria,(100, ALTO_VENTANA // 2))
                pantalla.blit(texto_victoria, (ANCHO_VENTANA // 2 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                pg.display.flip()
                pg.time.delay(3000)

            
            #tiempo de juego
            tiempo_juego = font.render(f"Tiempo Restante {tiempo_restante}", True, (0,0,0))
            texto_puntaje = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (0,0,0))
            texto_vidas = font.render(f"x: {self.luffy.vidas}", True, (0,0,0))
            
            #colision enemigos con balas y estructuras
            for bala in self.luffy.bala_grupo:
                colision_bala_con_enemigo = pg.sprite.spritecollide(bala, grupo_enemigos, True)
                
                
                for enemigo in colision_bala_con_enemigo:
                    self.puntaje.muerte_enemiga(enemigo.puntaje)
                    bala.kill()
                    
                if  len(grupo_enemigos) < 1:
                    juego_ejecutandose =  False
                    pantalla.fill((0, 0, 0))
                    texto_victoria = font.render(f"Has logrado la... VICTORIA SOS CRACK", True, (255,255,255))
                    texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                    pantalla.blit(texto_puntaje_victoria,(0, ALTO_VENTANA // 2))
                    pantalla.blit(texto_victoria, (480 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                    pg.display.flip()
                    pg.time.delay(3000)

                
                #colision bala con estructura
                colision_bala_en_estructura =  pg.sprite.spritecollide(bala, lista_estructuras,False)
                for estructura in colision_bala_en_estructura:
                    bala.kill()

                #colision bala con trampa
                colision_bala_trampa = pg.sprite.spritecollide(bala, grupo_trampas, True)
                for trampa in colision_bala_trampa:
                    self.puntaje.destruir_trampa(trampa.puntaje)
                    bala.kill()

            #colision jugador con item
            colision_con_item = pg.sprite.spritecollide(self.luffy, grupo_items, True)
            for item in colision_con_item:
                if item == item_puntaje_1:
                    self.puntaje.agarrar_item(item.puntaje)
                elif item == item_vida_1:
                    self.luffy.agarrar_vida()


            #colision de personaje con estructuras
            for estructura in lista_estructuras:
                if self.luffy.verificar_colision([estructura]):
                    self.luffy.ajustar_a_plataforma(estructura.get_rect())


            #vulnerabilidad de personaje
            if self.luffy.invulnerable:
                tiempo_transcurrido = pg.time.get_ticks() - self.luffy.tiempo_invulnerable_actual
                if tiempo_transcurrido >= self.luffy.tiempo_invulnerable:
                    self.luffy.invulnerable = False
                
            #persona con enemigo colision
            colision_personaje_con_enemigo = pg.sprite.spritecollide(self.luffy, grupo_enemigos, False)
            for colision in colision_personaje_con_enemigo:
                
                if not self.luffy.invulnerable:
                    self.luffy.perdida_de_vidas()
            if self.luffy.vidas < 1:
                    juego_ejecutandose = False
                    pantalla.fill((0, 0, 0))
                    texto_victoria = font.render(f"Te han Matado... DERRORTA", True, (255,255,255))
                    texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                    pantalla.blit(texto_puntaje_victoria,(100, ALTO_VENTANA // 2))
                    pantalla.blit(texto_victoria, (ANCHO_VENTANA // 2 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                    pg.display.flip()
                    pg.time.delay(3000)

            
            #colision jugador con trampa
            colision_jugador_con_trampa = pg.sprite.spritecollide(self.luffy, grupo_trampas, False)
            for trampa in colision_jugador_con_trampa:
                
                if not self.luffy.invulnerable:
                    self.luffy.perdida_de_vidas()
            if self.luffy.vidas < 1:
                    juego_ejecutandose = False
                    pantalla.fill((0, 0, 0))
                    texto_victoria = font.render(f"Te han Matado... DERRORTA", True, (255,255,255))
                    texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                    pantalla.blit(texto_puntaje_victoria,(100, ALTO_VENTANA // 2))
                    pantalla.blit(texto_victoria, (ANCHO_VENTANA // 2 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                    pg.display.flip()
                    pg.time.delay(3000)
            


            pantalla.blit(fondo, fondo.get_rect())
            pantalla.blit(tiempo_juego,(ANCHO_VENTANA//2, 10))
            
            estructura1.draw(pantalla)
            estructura2.draw(pantalla)
            estructura3.draw(pantalla)
            estructura4.draw(pantalla)
            
            
            self.luffy.draw(pantalla)
            grupo_items.draw(pantalla)
            grupo_enemigos.draw(pantalla)
            grupo_trampas.draw(pantalla)
            self.luffy.update(delta_ms, lista_eventos, pantalla, lista_estructuras)
            self.luffy.gravedad_activa()
            
            
            pantalla.blit(self.icono_vida,(0, 35))
            pantalla.blit(texto_puntaje, (10, 15))
            pantalla.blit(texto_vidas, (25,35))
            grupo_items.update()
            grupo_enemigos.update()
            grupo_trampas.update()
            pg.display.update()
            
        #juego.parar_musica() 
    pg.quit()


