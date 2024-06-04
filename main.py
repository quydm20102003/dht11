from adapter.mqtt import MQTTClient
from flask import Flask, jsonify
import sqlite3
from datetime import datetime
import threading
from adapter.database import TemperatureDatabase
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# Initialize the database


@app.route('/data/all', methods=['GET'])
def get_all_data():
    """Endpoint to get all temperature data."""
    db = TemperatureDatabase()
    data = db.get_all_data()
    db.close()
    return jsonify(data)

@app.route('/data/latest', methods=['GET'])
def get_latest_data():
    """Endpoint to get the latest temperature data."""
    db = TemperatureDatabase()
    data = db.get_latest_data()
    db.close()
    return jsonify(data)


if __name__ == "__main__":
    broker_address = "localhost"
    port = 1883
    topic = "sensor/sensor1/temperature"
    
    mqtt_client = MQTTClient(broker_address, port, topic)
   

    conn = threading.Thread(target= mqtt_client.connect)
    conn.start()
    # db.save_temperature(23.5)
    # db.save_temperature(24.1)
    # all_data = db.get_all_data()
   
    
    # print("\nLatest Data:")
    # print(latest_data)
    



    try:
        app.run()
    except KeyboardInterrupt:
        mqtt_client.disconnect()