# ATLAS-ISF: Advanced IIoT Data Processing System

ATLAS-ISF is an industrial-grade server-side application designed for **Industrial Internet of Things (IIoT)** environments. It provides real-time data processing, advanced noise reduction, robust data storage, and AI-powered insights, tailored to manufacturing use cases.

## 🎯 Objectives

- **Real-Time Data Management**: Handle continuous streams of machine-generated data.
- **Noise Reduction**: Use **Kalman filtering** to clean sensor data.
- **Reliable Storage**: Employ TimescaleDB, Vector DB, and AWS RDS for multi-tier data storage.
- **AI Insights**: Integrate **local Mistral LLM** for advanced data analytics.
- **Comprehensive APIs**: Provide seamless data retrieval for multiple use cases.

---

## 🔧 Technical Architecture

### Core Components

- **Backend**: Built with **FastAPI** for high performance.
- **Data Transmission**: Real-time **WebSocket-based** communication.
- **Databases**:
  - **TimescaleDB**: For aggregate and buffer storage.
  - **Vector DB**: For detailed and structured sensor data.
  - **AWS RDS**: For long-term data storage.
- **AI Model**: Local **Mistral LLM** with **Retrieval-Augmented Generation (RAG)**.
- **Interface**: **Chainlit-powered conversational AI**.

### Key Features

#### Data Ingestion

- Supports diverse sensors: Force, temperature, vibration, acoustic emission, material properties, quality metrics and Efficient handling of diverse manufacturing data streams.

#### Data Processing

- Real-time **noise filtering** ,Outlier detection and statistical processing and Continuous aggregate generation.

#### Database Management

- Short-term buffer storage with 2-minute updates, Detailed vectorized data logging and Hourly aggregation into AWS RDS for archival.

#### AI-Powered Analytics

- Context-aware, document-based expert insights and Adaptive learning using local manufacturing datasets.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**, Docker, FastAPI, Ollama, TimescaleDB, Vector Database.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ATLAS-ISF.git
   cd ATLAS-ISF
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start Docker containers:
   ```bash
   docker-compose up -d
   ```
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

---

## 📡 API Overview

### Available Endpoints

- `/data/machine-info`
- `/data/process-parameters`
- `/data/sensor-readings/{sensor_type}` (e.g., forces, temperatures, vibrations, etc.)
- `/data/material-properties`
- `/data/quality-metrics`

### Conversational Interface

Access the AI chat interface at: `https://localhost:8000/chat`

---
