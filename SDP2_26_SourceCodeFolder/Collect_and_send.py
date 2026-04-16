#CollectData.py
import RPi.GPIO as GPIO
import time
import socket

class Sensor:
    def __init__(self, filename, sensor_name):
        self.filename = filename
        self.sensor_name = sensor_name

    def read_data(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                return f"{timestamp}, {self.sensor_name}: {last_line.strip()}"
            else:
                return ""

    def send_data_to_server(self, server_ip, server_port):
        data = self.read_data()
        if data:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((server_ip, server_port))
                    s.sendall(data.encode())
                    print("Data sent to server successfully")
            except Exception as e:
                print(f"Error sending data to server: {e}")

class IRSensor(Sensor):
    def __init__(self, filename="/home/SDP2/Desktop/ir_data.txt", sensor_name="IR Sensor"):
        super().__init__(filename, sensor_name)

class UltrasonicSensor(Sensor):
    def __init__(self, filename="/home/SDP2/Desktop/ultrasonic_data.txt", sensor_name="Ultrasonic Sensor"):
        super().__init__(filename, sensor_name)

class WaterLevelSensor(Sensor):
    def __init__(self, filename="/home/SDP2/Desktop/water_data.txt", sensor_name="Water Level Sensor"):
        super().__init__(filename, sensor_name)

class TemperatureSensor(Sensor):
    def __init__(self, filename="/home/SDP2/Desktop/temperature_humidity_data.txt", sensor_name="Temperature Sensor"):
        super().__init__(filename, sensor_name)

def alternate_send(sensors, server_ip, server_port):
    while True:
        for sensor in sensors:
            sensor.send_data_to_server(server_ip, server_port)
            time.sleep(2)

if __name__ == "__main__":
    ir_sensor = IRSensor()
    ultrasonic_sensor = UltrasonicSensor()
    water_level_sensor = WaterLevelSensor()
    temperature_sensor = TemperatureSensor()

    # Example server IP and port
    server_ip = "192.168.0.143"
    server_port = 8888

    sensors = [ir_sensor, ultrasonic_sensor, water_level_sensor, temperature_sensor]

    # Alternate sending data from each sensor to the server every 2 seconds
    alternate_send(sensors, server_ip, server_port)