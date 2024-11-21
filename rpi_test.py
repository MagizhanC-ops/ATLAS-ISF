import asyncio
import websockets
import json
from datetime import datetime
import random 
import socket

async def send_sensor_data():
    # Replace with the IP address of your FastAPI server
    SERVER_URL = "ws://localhost:8000/ws"  # Change this to your server's IP and port
    
    while True:
        try:
            async with websockets.connect(SERVER_URL) as websocket:
                while True:
                    # Simulate sensor data (replace with actual sensor readings)
                    data = {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "forces": {
                            "fx": round(random.uniform(-20, 20), 2),
                            "fy": round(random.uniform(-20, 20), 2),
                            "fz": round(random.uniform(-20, 20), 2)
                        },
                        "device_id": socket.gethostname()  # Optional: add device identification
                    }
                    
                    # Send data
                    await websocket.send(json.dumps(data))
                    print(f"Sent data: {data}")
                    
                    # Wait for 2 seconds
                    await asyncio.sleep(2)
        
        except (websockets.exceptions.ConnectionClosed, OSError) as e:
            print(f"Connection error: {e}")
            print("Attempting to reconnect in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

def main():
    asyncio.run(send_sensor_data())

if __name__ == "__main__":
    main()