import picamera 
from datetime import datetime
import cv2
import numpy as np
import pathlib
import .env

def enviarDatos(estadoAgua, estadoLuz):
    return [estadoAgua, estadoLuz]