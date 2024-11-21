from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import json
from datetime import datetime
import asyncio

app = FastAPI()

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)

connection_manager = ConnectionManager()

# WebSocket endpoint to receive sensor data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            # Receive data from the client
            data = await websocket.receive_text()
            
            # Parse and log the received data
            try:
                parsed_data = json.loads(data)
                print(f"Received data: {parsed_data}")
                
                # Optional: You can add additional processing here
                # For example, store in a database, perform calculations, etc.
                
                # Broadcast to all connected clients if needed
                await connection_manager.broadcast(data)
            
            except json.JSONDecodeError:
                print("Invalid JSON received")
    
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print("Client disconnected")

# Optional: Simple HTML page to monitor WebSocket connections
@app.get("/")
async def get():
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>WebSocket Monitor</title>
        </head>
        <body>
            <h1>WebSocket Data Monitor</h1>
            <div id="messages"></div>
            <script>
                var ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('pre');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html)

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    