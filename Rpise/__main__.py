import asyncio
from . import hardware
from . import websocket

def main():
    hardware.setup()
    try:
        asyncio.get_event_loop().run_until_complete(websocket.connect_and_listen())
    except KeyboardInterrupt:
        pass
    finally:
        hardware.GPIO.cleanup()

if __name__ == "__main__":
    main()
    