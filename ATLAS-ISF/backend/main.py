from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.endpoints import websocket_routes, rag_routes, data_routes
from backend.services.scheduler import SchedulerService
import uvicorn

app = FastAPI(title="ATLAS-ISF", version="1.0")
scheduler = SchedulerService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(websocket_routes.router)
app.include_router(rag_routes.router)
app.include_router(data_routes.router)

@app.on_event("startup")
async def startup_event():
    """Start scheduler on application startup"""
    await scheduler.start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    """Stop scheduler on application shutdown"""
    scheduler.stop_scheduler()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to ATLAS-ISF API"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True) 