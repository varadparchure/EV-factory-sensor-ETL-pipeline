from fastapi import FastAPI, HTTPException
import psycopg2
import json

app = FastAPI()

# Function to get a connection to Postgres.
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="postgres",  # Docker service name for Postgres
            database="factory_db",
            user="factory_user",
            password="factory_pass"
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection error: {e}")

@app.get("/sensor-data")
def read_sensor_data():
    conn = get_db_connection()
    cur = conn.cursor()
    # Query to get the latest 100 sensor records
    cur.execute("SELECT id, station, data, created_at FROM sensor_data ORDER BY created_at DESC LIMIT 100;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert the rows into a list of dictionaries
    results = []
    for row in rows:
        # row[2] is stored as JSONB in Postgres, which psycopg2 should return as a Python dict
        record = {
            "id": row[0],
            "station": row[1],
            "data": row[2],  # already a dict if using JSONB; otherwise, use json.loads(row[2])
            "created_at": row[3].isoformat() if row[3] else None
        }
        results.append(record)
    return results
