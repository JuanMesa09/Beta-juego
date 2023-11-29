import pygame as pg 
from constantes import *
from clase_jugador import Jugador
from clase_estructura import Estructura
from clase_nivel import Nivel

class Game():
    def __init__(self) -> None:
        self.__timer = 10
        
    def correr_nivel(self, stage_name:str):
        pg.init()
        screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        titulo = pg.display.set_caption("The Game")

        
        juego = Nivel(screen, ANCHO_VENTANA, ALTO_VENTANA, stage_name)
        juego.play_music()  
        vuelta = juego.stage_name
        
        clock = pg.time.Clock()

        back_img = pg.image.load('./image/img_fondo/goku_house.png')
        back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

        bullet_group =  pg.sprite.Group()
        juego_ejecutandose = True

        vegeta = Jugador(400, 200, frame_rate=70, speed_walk=20)

        estructura1 = Estructura(100, 250, 50, 50, './image/img_plataformas/plataforma_1.png')
        estructura2 = Estructura(300, 250, 50, 50, './image/img_plataformas/plataforma_1.png')

        while juego_ejecutandose:
            delta_ms = clock.tick(FPS)
            pg.time.delay(20)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        vegeta._Jugador__is_jumping = True
                        vegeta._Jugador__jumpCount = 10
                    elif event.key == pg.K_r:
                        vegeta.animacion_disparo('Right' if vegeta._Jugador__is_looking_right else 'Left')
                        bullet_group.add(vegeta.crear_proyectil())
                elif event.type == pg.QUIT:
                    print('Estoy CERRANDO el JUEGO')
                    juego_ejecutandose = False
                    break

            lista_teclas_presionadas = pg.key.get_pressed()
            if lista_teclas_presionadas[pg.K_d] and not lista_teclas_presionadas[pg.K_a]:
                vegeta.caminar('Right')
            elif lista_teclas_presionadas[pg.K_a] and not lista_teclas_presionadas[pg.K_d]:
                vegeta.caminar('Left')
            else:
                vegeta.estatico()

            if vegeta._Jugador__is_jumping:
                vegeta.jump()
            
            screen.blit(back_img, back_img.get_rect())
            estructura1.draw(screen)
            estructura2.draw(screen)

            for estructura in [estructura1, estructura2]:
                if vegeta.verificar_colision([estructura]):
                    vegeta.ajustar_a_plataforma(estructura.get_rect())

            bullet_group.draw(screen) 
            vegeta.actualizar_estado(delta_ms)
            vegeta.draw(screen)
            vegeta.do_animation(delta_ms)
            vegeta.do_movement(delta_ms)
            bullet_group.update()
            pg.display.update()
        
        juego.stop_music() 
    pg.quit()