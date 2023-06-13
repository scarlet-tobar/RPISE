import websockets
import json
from env import WS_SERVER_URL
import gpio

def parse_message(message):
    """
    Intenta convertir un mensaje de entrada en formato json a diccionario de python
    """
    try:
        return json.loads(message)
    except ValueError:
        print("Couldn't handle message")
        return None

def event(value):
    """
    Decorador para manejar mensajes que tengan clave { "event": <nombre> }
    De coincidir con value, ejecuta el handler. De lo contrario, continua el pipeline.
    """
    def decorator(func):
        def wrapper(message:dict):
            if message.get("event") == value:
                func(message)
                return True
        return wrapper
    return decorator

@event("SET_PIN")
def handle_pin_activator(data:dict):
    """
    Evento que se activa para modificar el valor de un pin.
    """
    pinname = data.get("pinname")
    assert pinname is not None
    
    value = data.get("value")
    assert value is not None
    
    gpio.named_output(pinname, value)

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
        if h(event):
            break

async def connect_and_listen():
    """
    Se conecta con el servidor de WebSocket y está listo para recibir mensajes.
    """
    async with websockets.connect(WS_SERVER_URL) as websocket:
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
