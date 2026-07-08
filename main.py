import random
import statistics
import time
from collections import deque

# Configuration for the simulation
METRIC_NAME = "Service Error Rate (%)"
NORMAL_MEAN = 2.0
NORMAL_STD_DEV = 0.5
ANOMALY_THRESHOLD_Z_SCORE = 3.0 # How many standard deviations from the mean to consider an anomaly
SIMULATION_INTERVAL_SECONDS = 0.5
DATA_WINDOW_SIZE = 20 # Number of recent data points to consider for statistics
ANOMALY_CHANCE_PERCENT = 10 # Percentage chance for a random anomaly to occur

def generate_metric_value(is_anomaly_event=False):
    """Simulates a metric value, occasionally introducing a clear anomaly."""
    if is_anomaly_event:
        # Generate a value significantly higher than normal to simulate an anomaly
        return random.uniform(NORMAL_MEAN + ANOMALY_THRESHOLD_Z_SCORE * NORMAL_STD_DEV * 1.5,
                              NORMAL_MEAN + ANOMALY_THRESHOLD_Z_SCORE * NORMAL_STD_DEV * 2.5)
    else:
        # Generate a normal value with some natural variance
        return max(0, random.gauss(NORMAL_MEAN, NORMAL_STD_DEV)) # Error rates can't be negative

def detect_anomaly(data_window, current_value):
    """
    Detects anomalies in the current_value based on the historical data_window.
    This simulates a simplified AI/ML model for anomaly detection in DevOps monitoring.
    """
    if len(data_window) < 2: # Need at least two points to calculate std dev
        return False, "Not enough data for anomaly detection."

    try:
        mean = statistics.mean(data_window)
        std_dev = statistics.stdev(data_window)
    except statistics.StatisticsError:
        # Handle cases where std_dev might be zero (e.g., all values are identical)
        return False, "Standard deviation is zero, no variance to detect."

    if std_dev == 0: # If all values are the same, no deviation possible
        return False, "Standard deviation is zero, no variance to detect."

    # Calculate the Z-score for the current value
    z_score = (current_value - mean) / std_dev

    # Check if the absolute Z-score exceeds the defined threshold
    if abs(z_score) > ANOMALY_THRESHOLD_Z_SCORE:
        return True, f"Z-score: {z_score:.2f} (Threshold: {ANOMALY_THRESHOLD_Z_SCORE})"
    return False, f"Z-score: {z_score:.2f}"

def main():
    print(f"--- AI-Enhanced DevOps Monitoring Simulation ({METRIC_NAME}) ---")
    print(f"Monitoring {METRIC_NAME} for anomalies using a {DATA_WINDOW_SIZE}-point rolling window.")
    print(f"Anomaly threshold: {ANOMALY_THRESHOLD_Z_SCORE} standard deviations from the mean.\n")

    # Use a deque for efficient rolling window management
    metric_history = deque(maxlen=DATA_WINDOW_SIZE)
    iteration = 0

    while True:
        iteration += 1
        # Simulate an anomaly event based on a random chance
        is_anomaly_event = random.randint(1, 100) <= ANOMALY_CHANCE_PERCENT
        current_metric = generate_metric_value(is_anomaly_event)

        # Add the current metric to our history window
        metric_history.append(current_metric)

        # --- AI-driven Anomaly Detection (simplified) ---
        # In a real DevOps scenario, this would be a more sophisticated ML model
        # analyzing various metrics, logs, and traces to predict or detect issues.
        is_anomaly, reason = detect_anomaly(list(metric_history), current_metric)

        status_message = f"[{iteration:04d}] {METRIC_NAME}: {current_metric:.2f}"

        if is_anomaly:
            # When an anomaly is detected, AI can trigger automated alerts,
            # auto-scaling, incident response workflows, or detailed diagnostics.
            print(f"{status_message} -> !!! ANOMALY DETECTED !!! ({reason})")
        else:
            print(f"{status_message} (Normal)")

        time.sleep(SIMULATION_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
