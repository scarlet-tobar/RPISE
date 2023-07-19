import picamera 
from datetime import datetime
import cv2
import numpy as np
import pathlib
import RPi.GPIO as GPIO
from utils.env import GPIO_OUT_PINS
import gpio

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
	
def enviarEstadoAgua(): # Retorna Dateime, turbiedad, anomalía, luz en una lista
	luz=0
	pin = GPIO_OUT_PINS.get("AC_LIGHT")
	pin=GPIO.input(pin)
	if pin==1:
		luz=True
	else:
		luz=False
	img=cv2.imread(capturarColor(sacarFoto()))
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	negro=cv2.mean(hsv)
	verde = cv2.inRange(hsv, lower_range, upper_range)
	promedioHsv = cv2.mean(verde)
	saturation=promedioHsv[1]/255
	print(saturation)
	if saturation>0.80:
		print("Listo")
		return [datetime.now(), saturation, False, luz] #Dateime, turbiedad, anomalía, luz
	elif saturation>0.50:
		print("En proceso")
		return [datetime.now(), saturation, False, luz]
	elif saturation>0.20:
		print("Empezando")
		return [datetime.now(), saturation, False, luz]
	elif negro[2]/255 < 1:
		print("Error")
		return [datetime.now(), -1, True, luz] 

if __name__ == "__main__":
	import time
	print("Testing COLOR AGUA")
	gpio.init()
	gpio.named_output("VALVE",True)
	
	time.sleep(2)
	
	gpio.named_output("CAM_LIGHT_1",True)
	gpio.named_output("CAM_LIGHT_2",True)
	
	gpio.named_output("VALVE",False)

	time.sleep(0.1)	
	foto = sacarFoto()
	time.sleep(0.1)
	gpio.named_output("CAM_LIGHT_1",False)
	gpio.named_output("CAM_LIGHT_2",False)
	
	#mostrar(foto)
	

