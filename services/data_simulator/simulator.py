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

def main():
    # We'll point to Kafka at localhost:9092 later
    # but for now, you can just define the variable
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print(f"Starting chassis data simulation. Kafka at: {bootstrap_servers}")

    try:
        while True:
            chassis_data = generate_chassis_data()
            # We'll send it to a topic called "chassis_topic"
            producer.send("chassis_topic", chassis_data)
            producer.flush()

            print(f"Sent data: {chassis_data}")
            time.sleep(5)  # wait 5 seconds before sending next reading
    except KeyboardInterrupt:
        print("Stopping simulation.")

if __name__ == "__main__":
    main()
