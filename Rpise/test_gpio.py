import gpio
import time

def main():
    gpio.init()
    
    status = True
    while True: 
        try:
            gpio.named_output("CAM_LIGHT",status)
            gpio.named_output("VALVE",status)
            gpio.named_output("AC_LIGHT",status)
            print(f"STATUS = {status}")
            status = not status
            time.sleep(5)
        except KeyboardInterrupt:
            break
        except Exception as e:
            break
    print("END")
    gpio.cleanup()

if __name__ == "__main__":
    main()