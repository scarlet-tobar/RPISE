import picamera 
from datetime import datetime
import cv2
import numpy as np
import pathlib
import RPi.GPIO as GPIO
from utils.env import GPIO_OUT_PINS
from utils import gpio
import time


lower_range=np.array([31,0,0])
upper_range=np.array([74,255,255])

def take_photo(filename):
    try:
        cam = picamera.PiCamera()
        cam.capture(filename)
        cam.close()
        img = cv2.imread(filename)
        img = img[0:360,120:1160]
        cv2.imwrite(filename, img)
        return img
    except:
        return None

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


def linear_map_and_clamp(value, in_min, in_max, out_min, out_max):
    # Perform linear mapping
    mapped_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    # Clamp the value within the output range
    mapped_value = max(min(mapped_value, out_max), out_min)
    
    return mapped_value

def getWaterStatus(img):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Extract the green channel (Hue) from the HSV image
    green_channel = hsv[:, :, 0]
    
    # Calculate the average value of non-zero green pixels
    green_pixels = green_channel[green_channel > 0]
    if green_pixels.size == 0:
        avg_green = 0.0
    else:
        avg_green = np.mean(green_pixels)

    # Calculate the ratio of non-zero green pixels to all pixels
    total_pixels = green_channel.size
    green_pixel_count = np.count_nonzero(green_channel) #there is an error here. count just non-zero values
    pixel_count_ratio = green_pixel_count / total_pixels
    if pixel_count_ratio < 0.05:
        return 0
    else:
        return linear_map_and_clamp(avg_green,10,75,0,1)

def doWaterMeasure():
    gpio.init()
    gpio.named_output("VALVE",True)
    
    time.sleep(1)
    
    gpio.named_output("CAM_LIGHT_1",True)
    gpio.named_output("CAM_LIGHT_2",True)
    
    gpio.named_output("VALVE",False)

    time.sleep(0.1)	
    
    image = take_photo("measure.jpeg")
    if image is None:
        return [0,True]

    time.sleep(0.1)	
    
    gpio.named_output("CAM_LIGHT_1",False)
    gpio.named_output("CAM_LIGHT_2",False)
    is_black = is_dark(image,20)
    led_status = getLightStatus()
    
    green_filter = captureColor(image)
    water_status = getWaterStatus(green_filter)
    
    return [ water_status, is_black ]