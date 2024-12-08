import numpy as np
from ..models.sensor_data import MachineData
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class KalmanFilter:
    def __init__(self, process_variance=1e-5, measurement_variance=1e-2, initial_value=0):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimate = initial_value
        self.estimate_error = 1.0
        
    def update(self, measurement):
        # Prediction
        prediction = self.estimate
        prediction_error = self.estimate_error + self.process_variance
        
        # Update
        kalman_gain = prediction_error / (prediction_error + self.measurement_variance)
        self.estimate = prediction + kalman_gain * (measurement - prediction)
        self.estimate_error = (1 - kalman_gain) * prediction_error
        
        return self.estimate

class KalmanFilterManager:
    def __init__(self):
        self.filters: Dict[str, Dict[str, KalmanFilter]] = {}
    
    def _get_filter(self, machine_id: str, sensor_type: str) -> KalmanFilter:
        if machine_id not in self.filters:
            self.filters[machine_id] = {}
        
        if sensor_type not in self.filters[machine_id]:
            self.filters[machine_id][sensor_type] = KalmanFilter()
        
        return self.filters[machine_id][sensor_type]
    
    def filter_sensor_data(self, data: MachineData) -> MachineData:
        try:
            # Filter force readings
            forces = data.sensor_readings.forces
            data.sensor_readings.forces.fx = self._get_filter(data.machine_id, "force_x").update(forces.fx)
            data.sensor_readings.forces.fy = self._get_filter(data.machine_id, "force_y").update(forces.fy)
            data.sensor_readings.forces.fz = self._get_filter(data.machine_id, "force_z").update(forces.fz)
            
            # Filter temperature readings
            temps = data.sensor_readings.temperatures
            data.sensor_readings.temperatures.tool_temp = self._get_filter(
                data.machine_id, "tool_temp").update(temps.tool_temp)
            data.sensor_readings.temperatures.sheet_temp = self._get_filter(
                data.machine_id, "sheet_temp").update(temps.sheet_temp)
            
            # Filter vibration readings
            vib = data.sensor_readings.vibrations
            data.sensor_readings.vibrations.x_axis = self._get_filter(
                data.machine_id, "vib_x").update(vib.x_axis)
            data.sensor_readings.vibrations.y_axis = self._get_filter(
                data.machine_id, "vib_y").update(vib.y_axis)
            data.sensor_readings.vibrations.z_axis = self._get_filter(
                data.machine_id, "vib_z").update(vib.z_axis)
            
            return data
            
        except Exception as e:
            logger.error(f"Error in Kalman filtering: {str(e)}")
            return data 