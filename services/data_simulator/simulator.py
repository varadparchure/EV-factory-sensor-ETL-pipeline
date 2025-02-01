import os
import time
import random
import json
from kafka import KafkaProducer

def generate_chassis_data():
    """
    Simulate data from the chassis assembly station.
    For now, let's just return a dictionary with random values.
    """
    return {
        "station": "chassis",
        "timestamp": time.time(),
        "torque": round(random.uniform(50, 200), 2),     # Newton-meters
        "frame_alignment": round(random.uniform(0.90, 1.00), 3),  # ratio
        "part_count": random.randint(0, 5)              # how many parts assembled
    }

def generate_battery_data():
    return {
        "station": "battery",
        "timestamp": time.time(),
        "voltage": round(random.uniform(300, 400), 1),      # total voltage
        "temperature": round(random.uniform(20, 45), 1),    # Celsius
        "cell_test_result": random.choice(["PASS", "FAIL"])
    }

def generate_paint_data():
    return {
        "station": "paint",
        "timestamp": time.time(),
        "booth_temp": round(random.uniform(18, 25), 1),    # Celsius
        "booth_humidity": round(random.uniform(30, 70), 1),# %
        "paint_thickness": round(random.uniform(0.8, 1.2), 3) # mm
    }

def generate_quality_data():
    return {
        "station": "quality",
        "timestamp": time.time(),
        "inspection_result": random.choice(["PASS", "FAIL", "REWORK"]),
        "defect_count": random.randint(0, 3)
    }

def main():
    # We'll point to Kafka at localhost:9092 later
    # but for now, you can just define the variable
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print(f"Starting multi-station data simulation. Kafka at: {bootstrap_servers}")

    try:
        while True:
            # 1) Generate chassis data, send to "chassis_topic"
            chassis_data = generate_chassis_data()
            producer.send("chassis_topic", chassis_data)
            print(f"Sent chassis data: {chassis_data}")

            # 2) Generate battery data, send to "battery_topic"
            battery_data = generate_battery_data()
            producer.send("battery_topic", battery_data)
            print(f"Sent battery data: {battery_data}")

            # 3) Generate paint data, send to "paint_topic"
            paint_data = generate_paint_data()
            producer.send("paint_topic", paint_data)
            print(f"Sent paint data: {paint_data}")

            # 4) Generate quality data, send to "quality_topic"
            quality_data = generate_quality_data()
            producer.send("quality_topic", quality_data)
            print(f"Sent quality data: {quality_data}")

            # Flush to ensure messages are actually sent
            producer.flush()

            # Sleep for a few seconds before next cycle
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping simulation.")

if __name__ == "__main__":
    main()
