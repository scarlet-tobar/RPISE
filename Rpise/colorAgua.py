import picamera 
from datetime import datetime
import cv2
import numpy as np
import pathlib
import .env

lower_range=np.array([31,0,0])
upper_range=np.array([74,255,255])

def sacarFoto():
	camara = picamera.PiCamera()
	now = datetime.now()
	nombre=now.strftime("%Y-%m-%d-%H-%M-%S")  +".jpeg"
	foto=camara.capture(nombre)
	camara.close()
	return nombre
	
#sacarFoto()

def mostrar(foto):
	img=cv2.imread(foto)			    
	cv2.imshow("imagen",img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

#mostrar('2023-06-01-11-03-08.jpeg')

def capturarColor(foto):
	img=cv2.imread(foto)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_range, upper_range)
	imask = mask>0
	green = np.zeros_like(img, np.uint8)
	green[imask] = img[imask]
	nombre= pathlib.Path(foto).stem + ".jpeg"
	cv2.imwrite((nombre), green)
	return nombre
	
def enviarEstadoAgua(): # Retorna Dateime, turbiedad, anomalía en una lista
	img=cv2.imread(capturarColor(sacarFoto()))
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	negro=cv2.mean(hsv)
	if negro[2]/255 < 10:
		print("Error")
		return [datetime.now(), -1, True] #Dateime, turbiedad, anomalía
	verde = cv2.inRange(hsv, lower_range, upper_range)
	promedioHsv = cv2.mean(verde)
	saturation=promedioHsv[1]/255
	if saturation>80:
		print("Listo")
		return [datetime.now(), saturation/100, False]
	elif saturation>50:
		print("En proceso")
		return [datetime.now(), saturation/100, False]
	else:
		print("Empezando")
		return [datetime.now(), saturation/100, True]


