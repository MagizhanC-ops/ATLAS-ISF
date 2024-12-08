from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime

class ToolPosition(BaseModel):
    x: float
    y: float
    z: float

class Forces(BaseModel):
    fx: float
    fy: float
    fz: float

class Temperatures(BaseModel):
    tool_temp: float
    sheet_temp: float
    ambient_temp: float

class Vibrations(BaseModel):
    x_axis: float
    y_axis: float
    z_axis: float
    rms_amplitude: float

class AcousticEmission(BaseModel):
    amplitude: float
    frequency: float
    rms_value: float

class ProcessParameters(BaseModel):
    tool_position: ToolPosition
    feed_rate: float
    spindle_speed: float
    step_depth: float

class SensorReadings(BaseModel):
    forces: Forces
    temperatures: Temperatures
    vibrations: Vibrations
    acoustic_emission: AcousticEmission

class MaterialProperties(BaseModel):
    thickness: float
    material_type: str
    initial_temperature: float
    strain_rate: float

class QualityMetrics(BaseModel):
    surface_roughness: float
    thickness_variation: float
    springback_angle: float

class MachineData(BaseModel):
    machine_id: str
    timestamp: datetime
    process_parameters: ProcessParameters
    sensor_readings: SensorReadings
    material_properties: MaterialProperties
    quality_metrics: QualityMetrics 