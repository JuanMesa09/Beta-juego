
import pygame as pg

from constantes import *
from clase_jugador import Jugador
from clase_estructura import Estructura


screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()

back_img = pg.image.load('./image/img_fondo/goku_house.png')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

bullet_group =  pg.sprite.Group()
juego_ejecutandose = True

vegeta = Jugador(0, 0, frame_rate=70, speed_walk=20)

estructura1 = Estructura(100, 250, 50, 50, './image/img_plataformas/plataforma_1.png')
estructura2 = Estructura(300, 250, 50, 50, './image/img_plataformas/plataforma_1.png')


while juego_ejecutandose:
    delta_ms = clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                print("apreto una vez")
            elif event.key == pg.K_LSHIFT:
                
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

    bullet_group.update()
    pg.display.update()
    
pg.quit()