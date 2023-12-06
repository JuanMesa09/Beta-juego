

import json 

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 30
DEBUG = True
RUTA = './config/config.json'

RUTA_PARADO_D ='./imagenes/img_jugador/standar/paradito_derecha_1.png'
RUTA_PARADO_I = './imagenes/img_jugador/standar/paradito_izquierda.png'
RUTA_CAMINAR_D ='./imagenes/img_jugador/andar/correr_derecha.png'
RUTA_CAMINAR_I = './imagenes/img_jugador/andar/correr_izquierda.png'

def abrir_config():
    with open(RUTA, 'r', encoding= 'utf-8') as config:

        return json.load(config)
    

