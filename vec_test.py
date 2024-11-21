#Qdrant is running on port 6333 on localhost inside of a docker container.
#Working!

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
