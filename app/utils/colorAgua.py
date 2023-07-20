import picamera 
from datetime import datetime
import cv2
import numpy as np
import pathlib
import RPi.GPIO as GPIO
from utils.env import GPIO_OUT_PINS
import utils.gpio


lower_range=np.array([31,0,0])
upper_range=np.array([74,255,255])

def take_photo(filename):
	cam = picamera.PiCamera()
	cam.capture(filename)
	cam.close()
	img = cv2.imread(filename)
	img = img[0:360,120:1160]
	cv2.imwrite(filename, img)
	return img
	
def is_dark(image,threshold):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray_image) < threshold
    return brightness

def captureColor(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_range, upper_range)
	imask = mask>0
	green = np.zeros_like(img, np.uint8)
	green[imask] = img[imask]
	return green

def getLightStatus():
	p = [False,False]
	for i in (1,2):
		pin = GPIO_OUT_PINS.get("CAM_LIGHT_" + str(i) )
		p[i - 1] = GPIO.input(pin) 
	return p
	
def getWaterStatus(img):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Extract the green channel (Hue) from the HSV image
    green_channel = hsv[:, :, 0]
    
    # Calculate the average value of non-zero green pixels
    green_pixels = green_channel[green_channel > 0]
    avg_green = np.mean(green_pixels)
    
    # Calculate the ratio of non-zero green pixels to all pixels
    total_pixels = green_channel.size
    green_pixel_count = np.count_nonzero(green_channel) #there is an error here. count just non-zero values
    pixel_count_ratio = green_pixel_count / total_pixels
    
    return (avg_green, pixel_count_ratio)
