import paho.mqtt.client as mqtt
import time
import threading
import random
import json
class MQTTClient:
    def __init__(self, broker_address, port, topic, client_id="test_client"):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.client = mqtt.Client(self.client_id)

        # Attach event callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # self.client.subscribe(self.topic)
        # print(f"Subscribed to topic: {self.topic}")

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from broker")

    def publish(self, payload):
        self.client.publish(self.topic, payload)
        print(f"Published message: {payload} to topic: {self.topic}")

    def start_publishing(self,interval):
       
        def publish_periodically():
            while True:
                msg = '{ "temp": %s}' %random.randint(10, 40)
                self.publish(msg)
                time.sleep(interval)
        
        thread = threading.Thread(target=publish_periodically)
        thread.daemon = True
        thread.start()

# Example usage:
if __name__ == "__main__":
    broker_address = "localhost"
    port = 1883
    topic = "sensor/sensor1/temperature"
    interval = 3  # seconds

    mqtt_client = MQTTClient(broker_address, port, topic)
    mqtt_client.connect()
    
    mqtt_client.start_publishing(interval)

    try:
        while True:
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        mqtt_client.disconnect()
