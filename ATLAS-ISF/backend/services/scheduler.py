from fastapi import BackgroundTasks
from datetime import datetime, timedelta
import asyncio
import logging
from .aws_sync import AWSSyncService
from ..database import SessionLocal

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.background_tasks = BackgroundTasks()
        self.is_running = False
    
    async def start_scheduler(self):
        """Start the background scheduler"""
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self._run_scheduler())
    
    async def _run_scheduler(self):
        """Run scheduled tasks"""
        while self.is_running:
            try:
                # Get current time
                now = datetime.now()
                
                # If it's the start of an hour, run sync
                if now.minute == 0:
                    session = SessionLocal()
                    try:
                        sync_service = AWSSyncService(session)
                        await sync_service.sync_hourly_data()
                    finally:
                        session.close()
                
                # Wait until next check (every minute)
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in scheduler: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False 