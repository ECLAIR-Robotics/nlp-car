import socket
import sys
import threading
import time
import serial

class JoystickClient(threading.Thread):
    def __init__(self, car_ip, car_port, port='COM6', baudrate=9600):
        super().__init__()
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(3)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((car_ip, car_port))
        self.running = True

    def send_data(self, data):
        self.sock.sendall(data.encode('ascii'))

    def run(self):
        while self.running:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                try:
                    if line[0] == 'X':
                        self.stop()
                    else:
                        self.send_data(line)
                except ValueError:
                    print(f"Invalid line: {line}")

    def stop(self):
        self.running = False
        self.ser.close()
        self.sock.close()
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: python controller_client.py [Car IP] [Car Port]")

    car_ip = sys.argv[1]
    car_port = int(sys.argv[2])

    client = JoystickClient(car_ip, car_port)
    client.start()