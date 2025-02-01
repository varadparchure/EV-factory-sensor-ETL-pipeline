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

