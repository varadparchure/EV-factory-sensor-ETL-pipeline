# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first (for caching)
COPY services/data_simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the simulator code
COPY services/data_simulator/ ./

# By default, well use an environment variable for Kafka address
ENV KAFKA_BOOTSTRAP_SERVERS="localhost:9092"

# Run the simulator
CMD ["python", "simulator.py"]

