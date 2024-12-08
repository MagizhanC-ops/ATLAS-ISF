**Project Name**: ATLAS-ISF  
**Version**: 1.0  
**Author**: Magizhan C B 

## 1. Overview
ATLAS-ISF is an industrial-grade server-side application for IIoT needs. It processes machine-generated data in real-time, performs noise reduction and outlier handling, and stores structured data.


## 2. Objectives
- Recieve and transmit data effectively through websockets.
- Efficiently process and classify real-time machine data.  
- Provide noise reduction, outlier prediction, and robust data storage mechanisms.  
- Provide API's for retriving different sets of information individually or collectively.
- Store and retrieve data for analytics and queries using a locally hosted LLM and vector database.  


## 3. Functional Requirements
3.1 Backend server: hosted through FastAPI and should be accessible and orchestrate all the different pipelines involved in the process.
    3.1.1 The default “/” request to route to a webpage using Next.JS web page which would be built later, Build the end-point use endpoints wherever required.
    3.1.2 Include Websockets for communication of data from aggregated data source (a RsPi which aggregates all the data and sends it the server)
    3.1.3 The data being received would be in the format of.
```json
{
  "machine_id": "ISF-001",
  "timestamp": "2024-12-01T14:30:00.123456",
  "process_parameters": {
    "tool_position": {
      "x": 100,
      "y": 200,
      "z": 300
    },
    "feed_rate": 100,
    "spindle_speed": 200,
    "step_depth": 300
  },
  "sensor_readings": {
    "forces": {
      "fx": 100,
      "fy": 200,
      "fz": 300
    },
    "temperatures": {
      "tool_temp": 100,
      "sheet_temp": 200,
      "ambient_temp": 300
    },
    "vibrations": {
      "x_axis": 100,
      "y_axis": 200,
      "z_axis": 300,
      "rms_amplitude": 400
    },
    "acoustic_emission": {
      "amplitude": 500,
      "frequency": 600,
      "rms_value": 700
    }
  },
  "material_properties": {
    "thickness": 100,
    "material_type": "string",
    "initial_temperature": 200,
    "strain_rate": 300
  },
  "quality_metrics": {
    "surface_roughness": 100,
    "thickness_variation": 200,
    "springback_angle": 300
  }
}
```
	3.1.6 The data being received should be routed towards the kalman filter for noise reduction and the classification and filling algorithm as shown in the sample code. 
	3.1.7 The after processed data should have an endpoint from which it is to be routed to the databases running on docker. (Both postgres and vector databases running on docker).


3.2 Database: The data received on the end point should be stored in multiple databases as per the instructions and sample code provided.
	3.2.1 Create a buffer storage which records the data continuously, and updates the TimescaleDB database with an aggregate value (average) every 2 minutes that is running on docker. (Must be a separate storage for each different sensor as mentioned in the table schema) 
	3.2.2 Use the same buffer but don't use the average but rather ship the entire data to the vector database through using the statistical algorithm that is provided in the sample code.
    3.2.3 Agregate readings of 1 hour is to be sent to AWS RDS using the example code provided can be fetched from the values stored in the database.
        The schema for different tables are to be provided below which are to be followed while creation of the tables.
```sql
                  ## 1. Force
                  CREATE TABLE Force (
                      Machine_ID VARCHAR(255),
                      Job_ID VARCHAR(255),
                      Time_Stamp TIMESTAMP,
                      Fx DECIMAL(10,5),
                      Fy DECIMAL(10,5),
                      Fz DECIMAL(10,5),
                      PRIMARY KEY (Machine_ID, Job_ID, Time_Stamp),
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID),
                      FOREIGN KEY (Job_ID) REFERENCES Job_Details(Job_ID)
                  );

                  ## 2. Temperature
                  CREATE TABLE Temperature (
                      Machine_ID VARCHAR(255),
                      Job_ID VARCHAR(255),
                      Temperature DECIMAL(10,5),
                      Time_Stamp TIMESTAMP,
                      PRIMARY KEY (Machine_ID, Job_ID, Time_Stamp),
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID),
                      FOREIGN KEY (Job_ID) REFERENCES Job_Details(Job_ID)
                  );

                  ## 3. Vibration
                  CREATE TABLE Vibration (
                      Machine_ID VARCHAR(255),
                      Job_ID VARCHAR(255),
                      Vibration DECIMAL(10,5),
                      Time_Stamp TIMESTAMP,
                      PRIMARY KEY (Machine_ID, Job_ID, Time_Stamp),
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID),
                      FOREIGN KEY (Job_ID) REFERENCES Job_Details(Job_ID)
                  );

                  ## 4. Acoustic_Emission
                  CREATE TABLE Acoustic_Emission (
                      Machine_ID VARCHAR(255),
                      Job_ID VARCHAR(255),
                      Amplitude DECIMAL(10,5),
                      Frequency DECIMAL(10,5),
                      Time_Stamp TIMESTAMP,
                      PRIMARY KEY (Machine_ID, Job_ID, Time_Stamp),
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID),
                      FOREIGN KEY (Job_ID) REFERENCES Job_Details(Job_ID)
                  );

                  ## 5. Thickness
                  CREATE TABLE Thickness (
                      Machine_ID VARCHAR(255),
                      Job_ID VARCHAR(255),
                      Thickness DECIMAL(10,5),
                      Time_Stamp TIMESTAMP,
                      PRIMARY KEY (Machine_ID, Job_ID, Time_Stamp),
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID),
                      FOREIGN KEY (Job_ID) REFERENCES Job_Details(Job_ID)
                  );

                  ## 6. Surface_Roughness
                  CREATE TABLE Surface_Roughness (
                      Machine_ID VARCHAR(255),
                      Job_ID VARCHAR(255),
                      Surface_Roughness_Ra DECIMAL(10,7),
                      SA_Rz DECIMAL(10,7),
                      SA_Ry DECIMAL(10,7),
                      Time_Stamp TIMESTAMP,
                      PRIMARY KEY (Machine_ID, Job_ID, Time_Stamp),
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID),
                      FOREIGN KEY (Job_ID) REFERENCES Job_Details(Job_ID)
                  );

                  ## 7. Machine_Details (Reference Table)
                  CREATE TABLE Machine_Details (
                      Machine_ID VARCHAR(255) PRIMARY KEY,
                      Spindle_Range INT,
                      Model VARCHAR(255),
                      Type VARCHAR(255),
                      Max_X INT,
                      Max_Y INT,
                      Max_Z INT
                  );

                  ## 8. Material_Property (Reference Table)
                  CREATE TABLE Material_Property (
                      Material_ID VARCHAR(255) PRIMARY KEY,
                      Material_Name VARCHAR(255),
                      Youngs_Modulus DOUBLE,       -- N/mm²
                      Poisson_Ratio DOUBLE,        -- dimensionless
                      Yield_Strength DOUBLE,       -- N/mm²
                      Density DOUBLE,              -- kg/m³
                      Thermal_Conductivity DOUBLE, -- K⁻¹
                      Thermal_Expansion_Coefficient DOUBLE -- N/mK
                  );

                  ## 9. Job_Details (Reference Table)
                  CREATE TABLE Job_Details (
                      Job_ID VARCHAR(255) PRIMARY KEY,
                      Material_ID VARCHAR(255),
                      Thickness DOUBLE,
                      Initial_Temp DOUBLE,
                      FOREIGN KEY (Material_ID) REFERENCES Material_Property(Material_ID)
                  );

                  ## 10. Maintenance_Log (Optional)
                  CREATE TABLE Maintenance_Log (
                      Log_ID VARCHAR(255) PRIMARY KEY,
                      Machine_ID VARCHAR(255),
                      Run_Time TIME,
                      Maintenance_Date TIMESTAMP,
                      Description TEXT,
                      FOREIGN KEY (Machine_ID) REFERENCES Machine_Details(Machine_ID)
                  );
```
    ### Database Relationship Overview:
        - Machine_Details, Material_Property, and Job_Details serve as reference tables
        - All measurement tables (1-6) have composite primary keys (Machine_ID, Job_ID, Time_Stamp)
        - All measurement tables have foreign key relationships to both Machine_Details and Job_Details
        - Job_Details has a foreign key relationship to Material_Property
        - Maintenance_Log (optional) has a foreign key relationship to Machine_Details

3.3 RAG Model: Model developed based on locally running ollama server mistral model to infer data from the vector databases.
	3.3.1 Whenever FastAPI is reloaded it should check ./docs folder in root directory for any new applications, if so it should convert it and transfer it to the vector database.Choose optimal chunk size and other required parameters. 
	3.3.2 It should also be able to access the time series data being stored in the vectordb at the same time.
    3.3.3 It should always answer from a manufacturing expert perspective and should respond with an obvious message if no relevant information is found.
    3.3.4 Use chainlit interface for conversing with the database, also make sure that there is an API call which pulls the chain lit interface to the Ui when called at “https://localhost:8000/chat “ for this case.
    3.3.5 Customize the chainlit interface to suit the need of the project and make adjustments whereever required.
    3.3.6 Additionally it should be able to load up documents into the vector database from a fixed local directory as a source of knowledge. FYI the documents are in the ./docs folder and would contain books, research articles, etc. The knowledge update should be done when the chainlit interface is loaded.


3.4  FastAPI Endpoints: 
    3.4.1 Each endpoint should be cabable of fetching the latest value from the database and sending it to the requested client in a JSON format. as mentioned bellow, create the request to retive the  latest data from the required table and send it.
```python
    @app.get("/data/machine-info")
    @app.get("/data/process-parameters")
    @app.get("/data/sensor-readings/forces")
    @app.get("/data/sensor-readings/temperatures")
    @app.get("/data/sensor-readings/vibrations")
    @app.get("/data/sensor-readings/acoustic-emission")
    @app.get("/data/material-properties")
    @app.get("/data/quality-metrics")
```
    3.4.2 Each endpoint handles request indvidually. for the process parameters data should streamed directly instead of fetching it from the database.
    3.4.3 The get request should have an additional parameter of machine_id and job_id to filter the data accordingly that is supposed to be included in the request itself. 

# Documentation 
**Vectore Database Example**
```python
#Qdrant is running on port 6333 on localhost inside of a docker container.
import numpy as np
import datetime
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from scipy.stats import skew, kurtosis


# Connect to the Qdrant instance
client = QdrantClient(host="localhost", port=6333)
collection_name = "sensor_data_vectors"


# Create the collection (if not already created)
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=5, distance=Distance.COSINE)  # Vector size is 5 (statistical features)
)


# Helper function to compute statistical features
def compute_statistical_features(sensor_data):
    """
    Compute statistical features (mean, std, min, max, skewness, kurtosis) for a sensor's time-series data.
    Returns a feature vector with these values.
    """
    mean_val = np.mean(sensor_data)
    std_val = np.std(sensor_data)
    min_val = np.min(sensor_data)
    max_val = np.max(sensor_data)
    skew_val = skew(sensor_data)
    kurt_val = kurtosis(sensor_data)
    
    return [mean_val, std_val, min_val, max_val, skew_val]


## Instead of this real-time data is to be inputed
force_data_1 = [10.1, 12.3, 11.5, 9.8, 10.7, 11.9, 12.5]
temperature_data_1 = [100.2, 101.3, 99.5, 102.1, 101.7, 100.9, 100.5]


force_1_features = compute_statistical_features(force_data_1)
temperature_1_features = compute_statistical_features(temperature_data_1)


client.upsert(
    collection_name=collection_name,
    points=[
        {
            "id": 1,
            "vector": force_1_features,
            "payload": {
                "sensor_id": "force_sensor_1",
                "machine_id": "machine_001",
                "job_id": "job_001",
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
    ]
)


client.upsert(
    collection_name=collection_name,
    points=[
        {
            "id": 3,
            "vector": temperature_1_features,
            "payload": {
                "sensor_id": "temperature_sensor_1",
                "machine_id": "machine_001",
                "job_id": "job_001",
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
    ]
)


print("Data inserted successfully!")


**TimescaleDB Example**
#TimescaleDB is running on port 5002 on localhost inside of a docker container.
#Working!


from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


Base = declarative_base()


class Force(Base):
    __tablename__ = "force"
    machine_id = Column(String(255), primary_key=True, nullable=False)
    job_id = Column(String(255), primary_key=True, nullable=False)
    time_stamp = Column(DateTime, primary_key=True, nullable=False)
    fx = Column(Float, nullable=False)
    fy = Column(Float, nullable=False)
    fz = Column(Float, nullable=False)


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5002/postgres")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


new_force_data = Force(
    machine_id="machine_001",
    job_id="job_001",
    time_stamp=datetime.datetime.now(),
    fx=10.12345,
    fy=20.54321,
    fz=30.98765
)
session.add(new_force_data)
session.commit()


# Retrieve and display records from the Force table
retrieved_data = session.query(Force).all()
for data in retrieved_data:
    print(f"Machine_ID: {data.machine_id}, Job_ID: {data.job_id}, Time_Stamp: {data.time_stamp}, "
          f"Fx: {data.fx}, Fy: {data.fy}, Fz: {data.fz}")


**Classification Example**
import numpy as np


# Kalman Filter Class with Missing Value and Outlier Handling
class KalmanFilter:
    def __init__(self, process_var=1e-5, measurement_var=1e-2, outlier_threshold=10.0):
        self.process_var = process_var
        self.measurement_var = measurement_var
        self.outlier_threshold = outlier_threshold
        self.estimate = None
        self.error = 1.0


    def filter(self, value):
        if value is None:
            # Missing value: use prediction
            return self.estimate


        if self.estimate is not None and abs(value - self.estimate) > self.outlier_threshold:
            # Outlier detected: replace with predicted estimate
            value = self.estimate


        if self.estimate is None:
            # Initialize the filter with the first value
            self.estimate = value
        else:
            # Prediction step
            predicted_estimate = self.estimate
            predicted_error = self.error + self.process_var


            # Update step
            kalman_gain = predicted_error / (predicted_error + self.measurement_var)
            self.estimate = predicted_estimate + kalman_gain * (value - predicted_estimate)
            self.error = (1 - kalman_gain) * predicted_error


        return self.estimate


# Simulated sensor data with noise, missing values, and outliers
# Instead of this, Real time sensor values are to be used !


np.random.seed(42)
true_values = np.linspace(10, 50, 20)
noisy_fx = true_values + np.random.normal(0, 5, len(true_values))
noisy_fx[5] = None
noisy_fx[10] = 500.0


# Initialize Kalman filter
kalman_fx = KalmanFilter()


# Process data through Kalman filter
filtered_fx = [kalman_fx.filter(value) for value in noisy_fx]


# Display results
print("Original vs. Filtered Data (fx):")
for i, (original, filtered) in enumerate(zip(noisy_fx, filtered_fx)):
    print(f"Index {i:02}: Original: {original}, Filtered: {filtered:.2f}")


**FastAPI + WebSockets Example**
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import json
from datetime import datetime
import asyncio


app = FastAPI()


# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)


    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


connection_manager = ConnectionManager()


# WebSocket endpoint to receive sensor data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            # Receive data from the client
            data = await websocket.receive_text()
            
            # Parse and log the received data
            try:
                parsed_data = json.loads(data)
                print(f"Received data: {parsed_data}")
                
                # Optional: You can add additional processing here
                # For example, store in a database, perform calculations, etc.
                
                # Broadcast to all connected clients if needed
                await connection_manager.broadcast(data)
            
            except json.JSONDecodeError:
                print("Invalid JSON received")
    
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


**AWS Data Example**
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables
load_dotenv('.env.local')


def insert_force_data(data):
    try:
        # Establish connection
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname=os.getenv('DB_NAME')
        )
        
        # Create cursor
        cur = conn.cursor()
        
        # Create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS force_measurements (
                timestamp TIMESTAMPTZ PRIMARY KEY,
                fx FLOAT,
                fy FLOAT,
                fz FLOAT
            )
        """)
        
        # Insert data
        cur.execute("""
            INSERT INTO force_measurements 
            (timestamp, fx, fy, fz)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (
            data['timestamp'], 
            data['forces']['fx'], 
            data['forces']['fy'], 
            data['forces']['fz']
        ))
        
        # Commit and close
        conn.commit()
        cur.close()
        conn.close()
        print("Force data inserted successfully")
        
    except Exception as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    # Generate current timestamp and force data
    sample_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "forces": {
            "fx": 15.2,
            "fy": -9.8,
            "fz": 4.6
        }
    }
    insert_force_data(sample_data)


**Metrics Example**
import psutil
import time
import random


# Function to simulate operational status of a service
def get_service_status(service_name="example_service"):
    # Simulate operational status (Running, Stopped, or Unknown)
    statuses = ["Running", "Stopped", "Unknown"]
    return random.choice(statuses)


# Function to simulate data flow rate (in KB/s)
def get_data_flow_rate():
    # Simulate random data flow rates
    return random.uniform(10, 1000)  # KB/s


# Function to collect system metrics
def collect_metrics(service_name="example_service"):
    metrics = {
        "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "data_flow_rate_kbps": get_data_flow_rate(),
        "service_status": get_service_status(service_name)
    }
    return metrics


# Main loop to collect and display metrics
if __name__ == "__main__":
    service_name = "example_service"
    print(f"Monitoring service: {service_name}")
    print("=" * 50)


    try:
        while True:
            metrics = collect_metrics(service_name)
            print(f"CPU Usage: {metrics['cpu_usage_percent']:.2f}%")
            print(f"Memory Usage: {metrics['memory_usage_percent']:.2f}%")
            print(f"Data Flow Rate: {metrics['data_flow_rate_kbps']:.2f} KB/s")
            print(f"Service Status: {metrics['service_status']}")
            print("-" * 50)
            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
```

# ATLAS-ISF Project File Structure

## Root Directory
```plaintext
ATLAS-ISF/
│
├── backend/                    # Backend logic
│   ├── main.py                 # Entry point for FastAPI application
│   ├── endpoints/              # Organized API endpoints
│   │   ├── data_routes.py      # Routes for data processing and retrieval
│   │   ├── websocket_routes.py # Routes for WebSocket connections
│   │   └── rag_routes.py       # Routes for RAG (retrieval and inference) functionalities
│   ├── services/               # Core logic for backend services
│   │   ├── noise_filter.py     # Kalman filter for noise reduction
│   │   ├── db_operations.py    # TimescaleDB and Qdrant interactions
│   │   ├── vector_operations.py# Vector DB ingestion and querying
│   │   └── rag_inference.py    # RAG inference logic using Chainlit and LLM
│   ├── chainlit_interface.py   # Chainlit application for interactive RAG queries
│   ├── config.py               # Configuration (database, environment variables)
│
├── database/                   # Database-related files
│   ├── schema.sql              # SQL schema for TimescaleDB
│   └── docker-compose.yml      # Docker setup for TimescaleDB and Qdrant
│
├── rag/                        # Dedicated folder for RAG knowledge management
│   ├── docs_ingestion.py       # Logic to process and ingest documents into Qdrant
│   └── vector_store_config.py  # Configuration for vector database management
│
├── docs/                       # Documentation folder for knowledge ingestion
│   ├── guide1.pdf              # Reference guide or research paper
│   └── paper1.pdf              # Additional reference material
│
├── ui/                         # Placeholder for front-end integration
│   └── index.html              # Simple placeholder for initial UI rendering
│
├── Dockerfile                  # Dockerfile for containerizing the FastAPI app
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables for local development
└── README.md                   # Project-level documentation

## Rules
Make sure all the sensor values are being included in any part of the program wherever required.
Also make sure that no values are simulated; everything should be based on the real-time values that are received from the web sockets traveling through different pipelines.
Keep in mind that this is a fully functional app not a mock app using any mock data, never use any simulated or assumed data, if some data is required to be inserted mark that and let me know instead of filling it. 



