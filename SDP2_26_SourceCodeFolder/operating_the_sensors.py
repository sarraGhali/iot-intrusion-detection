#IR.py
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

#Distance.py
import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin 
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def read_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
        
        pulse_start = time.time()
        pulse_end = time.time()
        
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        return distance

if __name__ == "__main__":
    ultrasonic_sensor = UltrasonicSensor(7, 11)
    ULTRASONIC_FILE = "ultrasonic_data.txt"
    while True:
        distance = ultrasonic_sensor.read_distance()
        with open("ultrasonic_data.txt", "a") as file:
            file.write(str(distance) + "\n")
        time.sleep(2)

#waterSensor.py
import RPi.GPIO as GPIO
import time

class WaterSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    def read_data(self):
        return GPIO.input(self.pin)

if __name__ == "__main__":
    water_sensor = WaterSensor(18)
    WATER_FILE = "water_data.txt"
    while True:
        data = water_sensor.read_data()
        with open("water_data.txt", "a") as file:
            file.write(str(data) + "\n")
        time.sleep(2)

#Temp.py
import Adafruit_DHT
import time

class DHT22Sensor:
    def __init__(self, pin=4, sensor_type=Adafruit_DHT.DHT22, filename="/home/SDP2/Desktop/temperature_humidity_data.txt"):
        self.pin = pin
        self.sensor_type = sensor_type
        self.filename = filename

    def read_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)
        if humidity is not None and temperature is not None:
            return humidity, temperature
        else:
            return None, None

    def save_data_to_file(self, humidity, temperature):
        with open(self.filename, "a") as file:
            file.write(f"Humidity: {humidity:.2f}%, Temperature: {temperature:.2f}°C\n")

if __name__ == "__main__":
    dht_sensor = DHT22Sensor()

    try:
        while True:
            humidity, temperature = dht_sensor.read_data()
            if humidity is not None and temperature is not None:
                print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
                dht_sensor.save_data_to_file(humidity, temperature)
            else:
                print("Failed to read data from DHT sensor")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Measurement stopped by user")