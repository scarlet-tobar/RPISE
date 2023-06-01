import picamera 
from datetime import datetime
import cv2
import numpy as np

def sacarFoto():
	camara = picamera.PiCamera()
	now = datetime.now()
	foto=camara.capture(now.strftime("%Y-%m-%d-%H-%M-%S")  +".jpeg")
	camara.close()
	return foto
	
sacarFoto()
