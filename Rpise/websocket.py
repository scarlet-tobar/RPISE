import websockets
import json
from . import hardware
from . import env

def parse_message(message):
    try:
        return json.loads(message)
    except ValueError:
        print("Couldn't handle message")
        return None

def event(value):
    def decorator(func):
        def wrapper(message:dict):
            if message.get("event") != value:
                raise AssertionError(f"Invalid event. Expected '{value}', got '{message.get('event')}'")
            return func(message)
        return wrapper
    return decorator

@event("PIN")
def handle_pin_activator(data:dict):
    pinname = data.get("pin")
    assert pinname is not None
    
    pin = hardware.OUT_PINS.get(pinname)
    if pin is None: 
        valid_names = "', '".join(list(hardware.OUT_PINS.items()))
        raise AssertionError(f"<pinname> = '{pinname}' is not valid. Valid names: '{valid_names}'")
    
    value = data.get("value")
    assert value is not None
    
    hardware.output(pin, value)    

def handle_message(message):
    """
    Maneja todos los mensajes que llegan desde el servidor.
    El servidor debe mandar un mensaje con la estructura:
    {
        "event": <nombre del evento>,
        ** <datos adicionales> 
    }
    """
    data = parse_message(message)
    assert data is not None
    
    event = data.get("event")
    assert event is not None

    handlers = [
        handle_pin_activator,
        # more handlers here
    ]
    for h in handlers:
        h(event)

async def connect_and_listen():
    async with websockets.connect(env.WEBSOCKET_BACKEND) as websocket:
        print("Connected to WebSocket server")

        while True:
            try:
                message = await websocket.recv()
                handle_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed. Reconnecting...")
                break
            except Exception as e:
                print(f"Websocket error: {e}")
