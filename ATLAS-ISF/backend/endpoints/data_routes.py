from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..services.data_retrieval import DataRetrievalService
from ..database import get_db
import logging

router = APIRouter(prefix="/data")
logger = logging.getLogger(__name__)

@router.get("/machine-info")
async def get_machine_info(
    machine_id: str = Query(..., description="Machine ID"),
    db: Session = Depends(get_db)
):
    """Get machine information"""
    service = DataRetrievalService(db)
    data = service.get_machine_info(machine_id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Machine not found")

@router.get("/sensor-readings/forces")
async def get_forces(
    machine_id: str = Query(..., description="Machine ID"),
    job_id: Optional[str] = Query(None, description="Job ID"),
    db: Session = Depends(get_db)
):
    """Get latest force readings"""
    service = DataRetrievalService(db)
    data = service.get_latest_forces(machine_id, job_id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Force data not found")

@router.get("/sensor-readings/temperatures")
async def get_temperatures(
    machine_id: str = Query(..., description="Machine ID"),
    job_id: Optional[str] = Query(None, description="Job ID"),
    db: Session = Depends(get_db)
):
    """Get latest temperature readings"""
    service = DataRetrievalService(db)
    data = service.get_latest_temperatures(machine_id, job_id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Temperature data not found")

@router.get("/sensor-readings/vibrations")
async def get_vibrations(
    machine_id: str = Query(..., description="Machine ID"),
    job_id: Optional[str] = Query(None, description="Job ID"),
    db: Session = Depends(get_db)
):
    """Get latest vibration readings"""
    service = DataRetrievalService(db)
    data = service.get_latest_vibrations(machine_id, job_id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Vibration data not found")

@router.get("/sensor-readings/acoustic-emission")
async def get_acoustic_emission(
    machine_id: str = Query(..., description="Machine ID"),
    job_id: Optional[str] = Query(None, description="Job ID"),
    db: Session = Depends(get_db)
):
    """Get latest acoustic emission readings"""
    # TODO: Implement acoustic emission data retrieval
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/material-properties")
async def get_material_properties(
    machine_id: str = Query(..., description="Machine ID"),
    job_id: Optional[str] = Query(None, description="Job ID"),
    db: Session = Depends(get_db)
):
    """Get material properties"""
    # TODO: Implement material properties retrieval
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/quality-metrics")
async def get_quality_metrics(
    machine_id: str = Query(..., description="Machine ID"),
    job_id: Optional[str] = Query(None, description="Job ID"),
    db: Session = Depends(get_db)
):
    """Get quality metrics"""
    # TODO: Implement quality metrics retrieval
    raise HTTPException(status_code=501, detail="Not implemented yet") 