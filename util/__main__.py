import gpio
import colorAgua
import time
def main():
    gpio.init()
    try:
        gpio.named_output("VALVE",True)
        gpio.named_output("AC_LIGHT",True)
        gpio.named_output("CAM_LIGHT_1",True)
        gpio.named_output("CAM_LIGHT_2",True)
        while True:
            colorAgua.enviarEstadoAgua()
            time.sleep(60)

    finally:
        gpio.cleanup()


if __name__ == "__main__":
    main()
    
