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