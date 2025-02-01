import os
import time
import random
import json
from kafka import KafkaProducer

def generate_chassis_data():
    return {
        "station": "chassis",
        "timestamp": time.time(),
        "torque": round(random.uniform(50, 200), 2),
        "frame_alignment": round(random.uniform(0.90, 1.00), 3),
        "part_count": random.randint(0, 5)
    }

def generate_battery_data():
    return {
        "station": "battery",
        "timestamp": time.time(),
        "voltage": round(random.uniform(300, 400), 1),
        "temperature": round(random.uniform(20, 45), 1),
        "cell_test_result": random.choice(["PASS", "FAIL"])
    }

def generate_paint_data():
    return {
        "station": "paint",
        "timestamp": time.time(),
        "booth_temp": round(random.uniform(18, 25), 1),
        "booth_humidity": round(random.uniform(30, 70), 1),
        "paint_thickness": round(random.uniform(0.8, 1.2), 3)
    }

def generate_quality_data():
    return {
        "station": "quality",
        "timestamp": time.time(),
        "inspection_result": random.choice(["PASS", "FAIL", "REWORK"]),
        "defect_count": random.randint(0, 3)
    }

def create_producer(bootstrap_servers, retries=10, delay=5):
    """Attempt to create a KafkaProducer, retrying until successful or out of attempts."""
    for attempt in range(1, retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print(f"KafkaProducer created on attempt {attempt}")
            return producer
        except Exception as e:
            print(f"Attempt {attempt}: Kafka not ready ({e}). Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Kafka did not become available after multiple attempts.")

def main():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    print(f"Waiting for Kafka to be available at {bootstrap_servers}...")

    # Wait until Kafka is ready
    producer = create_producer(bootstrap_servers)

    print(f"Starting multi-station data simulation. Kafka at: {bootstrap_servers}")

    try:
        while True:
            # Generate and send chassis data
            chassis_data = generate_chassis_data()
            producer.send("chassis_topic", chassis_data)
            print(f"Sent chassis data: {chassis_data}")

            # Generate and send battery data
            battery_data = generate_battery_data()
            producer.send("battery_topic", battery_data)
            print(f"Sent battery data: {battery_data}")

            # Generate and send paint data
            paint_data = generate_paint_data()
            producer.send("paint_topic", paint_data)
            print(f"Sent paint data: {paint_data}")

            # Generate and send quality data
            quality_data = generate_quality_data()
            producer.send("quality_topic", quality_data)
            print(f"Sent quality data: {quality_data}")

            producer.flush()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping simulation.")

if __name__ == "__main__":
    main()
