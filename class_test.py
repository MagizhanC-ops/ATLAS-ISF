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
