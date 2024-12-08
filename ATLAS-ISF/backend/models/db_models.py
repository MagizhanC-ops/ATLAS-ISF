from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MachineDetails(Base):
    __tablename__ = "machine_details"
    
    machine_id = Column(String(255), primary_key=True)
    spindle_range = Column(Integer)
    model = Column(String(255))
    type = Column(String(255))
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)

class MaterialProperty(Base):
    __tablename__ = "material_property"
    
    material_id = Column(String(255), primary_key=True)
    material_name = Column(String(255))
    youngs_modulus = Column(Float)
    poisson_ratio = Column(Float)
    yield_strength = Column(Float)
    density = Column(Float)
    thermal_conductivity = Column(Float)
    thermal_expansion_coefficient = Column(Float)

class JobDetails(Base):
    __tablename__ = "job_details"
    
    job_id = Column(String(255), primary_key=True)
    material_id = Column(String(255), ForeignKey('material_property.material_id'))
    thickness = Column(Float)
    initial_temp = Column(Float)

class Force(Base):
    __tablename__ = "force"
    
    machine_id = Column(String(255), ForeignKey('machine_details.machine_id'), primary_key=True)
    job_id = Column(String(255), ForeignKey('job_details.job_id'), primary_key=True)
    time_stamp = Column(DateTime, primary_key=True)
    fx = Column(Float)
    fy = Column(Float)
    fz = Column(Float)

class Temperature(Base):
    __tablename__ = "temperature"
    
    machine_id = Column(String(255), ForeignKey('machine_details.machine_id'), primary_key=True)
    job_id = Column(String(255), ForeignKey('job_details.job_id'), primary_key=True)
    time_stamp = Column(DateTime, primary_key=True)
    tool_temp = Column(Float)
    sheet_temp = Column(Float)
    ambient_temp = Column(Float)

class Vibration(Base):
    __tablename__ = "vibration"
    
    machine_id = Column(String(255), ForeignKey('machine_details.machine_id'), primary_key=True)
    job_id = Column(String(255), ForeignKey('job_details.job_id'), primary_key=True)
    time_stamp = Column(DateTime, primary_key=True)
    x_axis = Column(Float)
    y_axis = Column(Float)
    z_axis = Column(Float)
    rms_amplitude = Column(Float)

class AcousticEmission(Base):
    __tablename__ = "acoustic_emission"
    
    machine_id = Column(String(255), ForeignKey('machine_details.machine_id'), primary_key=True)
    job_id = Column(String(255), ForeignKey('job_details.job_id'), primary_key=True)
    time_stamp = Column(DateTime, primary_key=True)
    amplitude = Column(Float)
    frequency = Column(Float)
    rms_value = Column(Float)

class QualityMetrics(Base):
    __tablename__ = "quality_metrics"
    
    machine_id = Column(String(255), ForeignKey('machine_details.machine_id'), primary_key=True)
    job_id = Column(String(255), ForeignKey('job_details.job_id'), primary_key=True)
    time_stamp = Column(DateTime, primary_key=True)
    surface_roughness = Column(Float)
    thickness_variation = Column(Float)
    springback_angle = Column(Float) 