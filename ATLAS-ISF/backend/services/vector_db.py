from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from ..models.sensor_data import MachineData
import numpy as np
from scipy.stats import skew, kurtosis
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self, collection_name="sensor_vectors"):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Ensure collection exists with correct settings"""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=15, distance=Distance.COSINE)
                )
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
    
    def _compute_statistical_features(self, data: MachineData) -> list[float]:
        """Compute statistical features from sensor data"""
        features = []
        
        # Force features
        forces = [
            data.sensor_readings.forces.fx,
            data.sensor_readings.forces.fy,
            data.sensor_readings.forces.fz
        ]
        features.extend([
            np.mean(forces),
            np.std(forces),
            skew(forces)
        ])
        
        # Temperature features
        temps = [
            data.sensor_readings.temperatures.tool_temp,
            data.sensor_readings.temperatures.sheet_temp,
            data.sensor_readings.temperatures.ambient_temp
        ]
        features.extend([
            np.mean(temps),
            np.std(temps),
            skew(temps)
        ])
        
        # Vibration features
        vibs = [
            data.sensor_readings.vibrations.x_axis,
            data.sensor_readings.vibrations.y_axis,
            data.sensor_readings.vibrations.z_axis
        ]
        features.extend([
            np.mean(vibs),
            np.std(vibs),
            skew(vibs)
        ])
        
        # Process parameters
        features.extend([
            data.process_parameters.feed_rate,
            data.process_parameters.spindle_speed,
            data.process_parameters.step_depth
        ])
        
        return features
    
    async def store_sensor_data(self, data: MachineData):
        """Store sensor data in vector database"""
        try:
            features = self._compute_statistical_features(data)
            
            point = PointStruct(
                id=str(datetime.now().timestamp()),
                vector=features,
                payload={
                    "machine_id": data.machine_id,
                    "timestamp": data.timestamp.isoformat(),
                    "material_type": data.material_properties.material_type,
                    "quality_metrics": data.quality_metrics.dict()
                }
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
        except Exception as e:
            logger.error(f"Error storing vector data: {str(e)}") 