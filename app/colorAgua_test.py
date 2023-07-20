from utils import gpio
from utils import colorAgua

if __name__ == "__main__":
	import time
	print("Testing COLOR AGUA")
	gpio.init()
	gpio.named_output("VALVE",True)
	
	time.sleep(1)
	
	gpio.named_output("CAM_LIGHT_1",True)
	gpio.named_output("CAM_LIGHT_2",True)
	
	gpio.named_output("VALVE",False)

	time.sleep(0.1)	
	
	image = colorAgua.take_photo("_capture.jpeg")
	time.sleep(0.1)	
	
	gpio.named_output("CAM_LIGHT_1",False)
	gpio.named_output("CAM_LIGHT_2",False)
	
	is_black = colorAgua.is_dark(image,20)
	print("IS BLACK",is_black)
	
	led_status = colorAgua.getLightStatus()
	print("LED STATUS:",led_status)
	
	green_filter = colorAgua.captureColor(image)
	# print("GREEN FILTER", green_filter)

	water_status = colorAgua.getWaterStatus(green_filter)
	print("WATER STATUS:",water_status)
	
	
	# mostrar(foto)
	