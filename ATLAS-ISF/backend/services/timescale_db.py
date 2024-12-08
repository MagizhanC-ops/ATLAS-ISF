from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..models.db_models import Base, Force, Temperature, Vibration
from ..models.sensor_data import MachineData
from ..config import get_settings
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)
settings = get_settings()

class TimescaleDBService:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{settings.TIMESCALE_DB_USER}:{settings.TIMESCALE_DB_PASSWORD}"
            f"@{settings.TIMESCALE_DB_HOST}:{settings.TIMESCALE_DB_PORT}/{settings.TIMESCALE_DB_NAME}"
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Buffer for aggregating data
        self.buffer = {
            'force': [],
            'temperature': [],
            'vibration': []
        }
        self.last_aggregate_time = datetime.now()
    
    def _should_aggregate(self) -> bool:
        """Check if 2 minutes have passed since last aggregation"""
        return (datetime.now() - self.last_aggregate_time) >= timedelta(minutes=2)
    
    def _aggregate_and_store(self):
        """Aggregate buffered data and store in TimescaleDB"""
        try:
            session = self.SessionLocal()
            
            # Process force data
            if self.buffer['force']:
                df_force = pd.DataFrame(self.buffer['force'])
                force_agg = df_force.groupby(['machine_id', 'job_id']).agg({
                    'fx': 'mean',
                    'fy': 'mean',
                    'fz': 'mean'
                }).reset_index()
                
                for _, row in force_agg.iterrows():
                    force_entry = Force(
                        machine_id=row['machine_id'],
                        job_id=row['job_id'],
                        time_stamp=datetime.now(),
                        fx=row['fx'],
                        fy=row['fy'],
                        fz=row['fz']
                    )
                    session.add(force_entry)
            
            # Similar aggregation for temperature and vibration...
            
            session.commit()
            
            # Clear buffer
            self.buffer = {
                'force': [],
                'temperature': [],
                'vibration': []
            }
            self.last_aggregate_time = datetime.now()
            
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            session.rollback()
        finally:
            session.close()
    
    def process_sensor_data(self, data: MachineData):
        """Process incoming sensor data"""
        try:
            # Add to buffer
            self.buffer['force'].append({
                'machine_id': data.machine_id,
                'job_id': 'default_job',  # You'll need to implement job management
                'fx': data.sensor_readings.forces.fx,
                'fy': data.sensor_readings.forces.fy,
                'fz': data.sensor_readings.forces.fz
            })
            
            # Check if it's time to aggregate
            if self._should_aggregate():
                self._aggregate_and_store()
                
        except Exception as e:
            logger.error(f"Error processing sensor data: {str(e)}") 