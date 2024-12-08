from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.websocket_manager import ConnectionManager
from ..services.noise_filter import KalmanFilterManager
from ..services.timescale_db import TimescaleDBService
from ..services.vector_db import VectorDBService
from ..models.sensor_data import MachineData
import json
import logging
from datetime import datetime
import uuid

router = APIRouter()
manager = ConnectionManager()
kalman_manager = KalmanFilterManager()
timescale_service = TimescaleDBService()
vector_service = VectorDBService()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.websocket("/ws/{machine_id}")
async def websocket_endpoint(websocket: WebSocket, machine_id: str):
    client_id = f"{machine_id}_{uuid.uuid4()}"
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse and validate the incoming data
                raw_data = json.loads(data)
                machine_data = MachineData(**raw_data)
                
                # Apply Kalman filtering to sensor readings
                filtered_data = kalman_manager.filter_sensor_data(machine_data)
                
                # Store in TimescaleDB
                timescale_service.process_sensor_data(filtered_data)
                
                # Store in Vector DB
                await vector_service.store_sensor_data(filtered_data)
                
                # Broadcast filtered data to all connected clients
                await manager.broadcast(filtered_data.dict())
                
            except Exception as e:
                logger.error(f"Error processing data: {str(e)}")
                await websocket.send_json({
                    "error": "Invalid data format",
                    "details": str(e)
                })
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(client_id) 