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
    
async def handle_message(message):
    data = parse_message(message)
    if data is None:
        return 
    
    pinname = data.get("pin")
    assert pinname is not None
    
    pin = hardware.OUT_PINS.get(pinname)
    if pin is None: 
        valid_names = "', '".join(list(hardware.OUT_PINS.items()))
        raise AssertionError(f"<pinname> = '{pinname}' is not valid. Valid names: '{valid_names}'")
    
    value = data.get("value")
    assert value is not None
    
    hardware.output(pin, value)

async def connect_and_listen():
    async with websockets.connect(env.WEBSOCKET_BACKEND) as websocket:
        print("Connected to WebSocket server")

        while True:
            try:
                message = await websocket.recv()
                await handle_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed. Reconnecting...")
                break
            except Exception as e:
                print(f"Websocket error: {e}")
