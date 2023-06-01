import picamera 
from datetime import datetime
import cv2
import numpy as np
camara = picamera.PiCamera()
now = datetime.now()
camara.capture(now.strftime("%Y-%m-%d-%H-%M-%S")  +".jpeg")
camara.close()
