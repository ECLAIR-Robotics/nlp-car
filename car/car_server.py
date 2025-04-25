import socket
import sys
from ecar import Car

def server(car_port, car):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', car_port))
    s.listen()
    print(f"Server listening on port {car_port}")
    try:
        while True:
            conn, _ = s.accept()
            with conn:
                while True:
                    data = conn.recv(8).decode('ascii')
                    if not data:
                        break
                    try:
                        x, y = map(int, data.split(','))
                        car.turn(x)
                        car.accel(y)
                    except ValueError:
                        print(f"Ignored invalid data: {data}")
                    continue
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        s.close()

def car_setup():
    servo_pin = 21
    motor1_pins = [27, 17]
    motor2_pins = [23, 24]
    return Car(servo_pin, motor1_pins, motor2_pins)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python car_server.py [Car Port]")
    car_port = int(sys.argv[1])
    car = car_setup()
    server(car_port, car)
