import boto3
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models.db_models import Force, Temperature, Vibration, AcousticEmission
from ..config import get_settings
import logging
import pandas as pd
import json

logger = logging.getLogger(__name__)
settings = get_settings()

class AWSSyncService:
    def __init__(self, session: Session):
        self.session = session
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_BUCKET_NAME
    
    def _get_hourly_aggregates(self, start_time: datetime) -> dict:
        """Get hourly aggregated data from TimescaleDB"""
        try:
            # Force data aggregation
            force_data = self.session.query(
                Force.machine_id,
                Force.job_id,
                func.avg(Force.fx).label('avg_fx'),
                func.avg(Force.fy).label('avg_fy'),
                func.avg(Force.fz).label('avg_fz'),
                func.min(Force.fx).label('min_fx'),
                func.min(Force.fy).label('min_fy'),
                func.min(Force.fz).label('min_fz'),
                func.max(Force.fx).label('max_fx'),
                func.max(Force.fy).label('max_fy'),
                func.max(Force.fz).label('max_fz')
            ).filter(
                Force.time_stamp >= start_time
            ).group_by(Force.machine_id, Force.job_id).all()
            
            # Similar aggregations for temperature, vibration, and acoustic emission
            # ... (implement similar queries)
            
            return {
                "timestamp": start_time.isoformat(),
                "force_data": [dict(row) for row in force_data],
                # Add other sensor data
            }
            
        except Exception as e:
            logger.error(f"Error aggregating hourly data: {str(e)}")
            return {}
    
    def _upload_to_s3(self, data: dict, timestamp: datetime):
        """Upload aggregated data to S3"""
        try:
            file_name = f"hourly_data/{timestamp.strftime('%Y-%m-%d_%H')}.json"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(data),
                ContentType='application/json'
            )
            
            logger.info(f"Successfully uploaded data to S3: {file_name}")
            
        except Exception as e:
            logger.error(f"Error uploading to S3: {str(e)}")
    
    async def sync_hourly_data(self):
        """Sync last hour's data to AWS"""
        try:
            # Get start of last hour
            start_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
            
            # Get aggregated data
            aggregated_data = self._get_hourly_aggregates(start_time)
            
            if aggregated_data:
                # Upload to S3
                self._upload_to_s3(aggregated_data, start_time)
                
        except Exception as e:
            logger.error(f"Error in hourly sync: {str(e)}") 