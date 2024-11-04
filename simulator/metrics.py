from prometheus_client import start_http_server, Gauge
import random
import time

def update_metrics():
    """
    Update example metrics with new values.
    """
    # Generate a random value and set it to the gauge
    random_value = random.uniform(0, 100)
    example_metric.set(random_value)
    print(f"Updated metric with random value: {random_value:.2f}")

def create_metric(id):
    """
    Create a new metric with the given id.
    """
    return Gauge(
        id,
        f"A gauge metric with id ${id}",
    )   

def start_server():
    start_http_server(8000)
    print("Metrics Server started on port 8000")
