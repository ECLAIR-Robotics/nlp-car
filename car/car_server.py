import socket
import sys
from ecar import Car

car = None
turn_value = 0    # from -100 to 100 (left to right)
speed_value = 0   # from -100 to 100 (reverse to forward)

def handle_mouse_control():
    global turn_value, speed_value

    if abs(speed_value) < 10:
        car.brake()
    elif speed_value > 0:
        car.forward(abs(speed_value))
    else:
        car.reverse(abs(speed_value))

    if abs(turn_value) < 10:
        car.reset_direction()
    elif turn_value < 0:
        car.turn_left(abs(turn_value))
    else:
        car.turn_right(abs(turn_value))

def server(car_port):
    global turn_value, speed_value
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

                    if data.startswith('x'):
                        try:
                            turn_value = int(data[1:])
                            handle_mouse_control()
                        except ValueError:
                            print(f"Ignored invalid turn value: {data}")
                        continue

                    if data.startswith('y'):
                        try:
                            speed_value = int(data[1:])
                            handle_mouse_control()
                        except ValueError:
                            print(f"Ignored invalid speed value: {data}")
                        continue
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        s.close()

def car_setup():
    servo_pin = 21
    motor1_pins = [27, 17]
    motor2_pins = [23, 24]
    global car
    car = Car(servo_pin, motor1_pins, motor2_pins)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python car_server.py [Car Port]")
    car_port = int(sys.argv[1])
    car_setup()
    server(car_port)
