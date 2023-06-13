"""
Este módulo tiene por objetivo controlar los periféricos:
- Luz de cámara
- Luz AC
- Válvula
""" 

import RPi.GPIO as GPIO
from . import env

OUT_PINS = {
    "VALVE" : env.GPIO_VALVE,
    "AC_LIGHT":  env.GPIO_AC_LIGHT,
    "CAM_LIGHT" : env.GPIO_CAM_LIGHT   
}

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in OUT_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def output(pin: int, value:bool):
    v = GPIO.HIGH if value else GPIO.LOW
    GPIO.output(pin, value)