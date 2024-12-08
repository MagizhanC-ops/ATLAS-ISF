from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.db_models import (
    Force, Temperature, Vibration, MachineDetails,
    MaterialProperty, JobDetails, AcousticEmission, QualityMetrics
)
import logging

logger = logging.getLogger(__name__)

class DataRetrievalService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_machine_info(self, machine_id: str) -> Optional[Dict[str, Any]]:
        """Get machine details"""
        try:
            machine = self.session.query(MachineDetails).filter(
                MachineDetails.machine_id == machine_id
            ).first()
            
            if machine:
                return {
                    "machine_id": machine.machine_id,
                    "spindle_range": machine.spindle_range,
                    "model": machine.model,
                    "type": machine.type,
                    "max_x": machine.max_x,
                    "max_y": machine.max_y,
                    "max_z": machine.max_z
                }
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving machine info: {str(e)}")
            return None
    
    def get_latest_forces(self, machine_id: str, job_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get latest force readings"""
        try:
            query = self.session.query(Force).filter(Force.machine_id == machine_id)
            if job_id:
                query = query.filter(Force.job_id == job_id)
            
            latest = query.order_by(desc(Force.time_stamp)).first()
            
            if latest:
                return {
                    "machine_id": latest.machine_id,
                    "job_id": latest.job_id,
                    "timestamp": latest.time_stamp.isoformat(),
                    "forces": {
                        "fx": latest.fx,
                        "fy": latest.fy,
                        "fz": latest.fz
                    }
                }
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving force data: {str(e)}")
            return None
    
    def get_latest_temperatures(self, machine_id: str, job_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get latest temperature readings"""
        try:
            query = self.session.query(Temperature).filter(Temperature.machine_id == machine_id)
            if job_id:
                query = query.filter(Temperature.job_id == job_id)
            
            latest = query.order_by(desc(Temperature.time_stamp)).first()
            
            if latest:
                return {
                    "machine_id": latest.machine_id,
                    "job_id": latest.job_id,
                    "timestamp": latest.time_stamp.isoformat(),
                    "temperature": latest.temperature
                }
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving temperature data: {str(e)}")
            return None
    
    def get_latest_vibrations(self, machine_id: str, job_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get latest vibration readings"""
        try:
            query = self.session.query(Vibration).filter(Vibration.machine_id == machine_id)
            if job_id:
                query = query.filter(Vibration.job_id == job_id)
            
            latest = query.order_by(desc(Vibration.time_stamp)).first()
            
            if latest:
                return {
                    "machine_id": latest.machine_id,
                    "job_id": latest.job_id,
                    "timestamp": latest.time_stamp.isoformat(),
                    "vibration": latest.vibration
                }
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving vibration data: {str(e)}")
            return None
    
    def get_latest_acoustic_emission(self, machine_id: str, job_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get latest acoustic emission readings"""
        try:
            query = self.session.query(AcousticEmission).filter(
                AcousticEmission.machine_id == machine_id
            )
            if job_id:
                query = query.filter(AcousticEmission.job_id == job_id)
            
            latest = query.order_by(desc(AcousticEmission.time_stamp)).first()
            
            if latest:
                return {
                    "machine_id": latest.machine_id,
                    "job_id": latest.job_id,
                    "timestamp": latest.time_stamp.isoformat(),
                    "acoustic_emission": {
                        "amplitude": latest.amplitude,
                        "frequency": latest.frequency,
                        "rms_value": latest.rms_value
                    }
                }
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving acoustic emission data: {str(e)}")
            return None
    
    def get_material_properties(self, machine_id: str, job_id: str) -> Optional[Dict[str, Any]]:
        """Get material properties for a specific job"""
        try:
            # Join JobDetails with MaterialProperty
            result = self.session.query(JobDetails, MaterialProperty).join(
                MaterialProperty,
                JobDetails.material_id == MaterialProperty.material_id
            ).filter(
                JobDetails.job_id == job_id
            ).first()
            
            if result:
                job, material = result
            return None 
        
        except Exception as e:
            logger.error(f"Error retrieving material properties: {str(e)}")
            return None