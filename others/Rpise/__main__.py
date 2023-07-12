import asyncio
import gpio
from ws import connect_and_listen

def main():
    gpio.init()

    try:
        asyncio.get_event_loop().run_until_complete(connect_and_listen())
    except KeyboardInterrupt:
        pass
    finally:
        gpio.cleanup()

if __name__ == "__main__":
    main()
    gpio.named_output("VALVE",True)
