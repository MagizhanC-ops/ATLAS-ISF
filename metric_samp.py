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
