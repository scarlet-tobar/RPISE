"""
Este módulo tiene por objetivo controlar los periféricos:
- Luz de cámara
- Luz AC
- Válvula
""" 

import RPi.GPIO as GPIO
from env import GPIO_OUT_PINS

def init():
    """
    Inicializa el GPIO, ajustando los pines de salida como tal.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in GPIO_OUT_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def cleanout():
    """
    Función helper para no importar GPIO.cleanout en otros modulos
    """
    GPIO.cleanout()

def named_output(pinname:str, value:bool):
    """
    Dado un nombre para un pin (definido en env.py), 
    comprueba que sea válido y luego setea el valor.
    """
    pin = GPIO_OUT_PINS.get(pinname)
    if pin is None: 
        valid_names = "', '".join(list(GPIO_OUT_PINS.items()))
        raise AssertionError(f"<pinname> = '{pinname}' is not valid. Valid names: '{valid_names}'")
    GPIO.output(pin,value)