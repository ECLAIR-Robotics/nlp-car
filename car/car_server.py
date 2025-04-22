import socket
import sys
from car.ecar import Car
speed = 0
angle = 0

car = None
keys_pressed = {'w': False, 'a': False, 's': False, 'd': False, ' ': False, 'x': False}

'''
def handle_keys():
    speed = 50
    if keys_pressed[' ']:
        speed = 100
    if keys_pressed['w']:
        car.forward(speed)
    elif keys_pressed['s']:
        car.reverse(speed)
    else:
        car.brake()
    if keys_pressed['a']:
        car.turn_left()
    elif keys_pressed['d']:
        car.turn_right()
    else:
        car.reset_direction()
'''

def handle_keys():
    if keys_pressed['w']:
        if speed <= 100:
            speed += 5
        car.forward(speed)
    elif keys_pressed['s']:
        if speed >= -100:
            speed -= 5
        car.reverse(speed)
    if keys_pressed['x']:
        car.brake()
    if keys_pressed['a']:
        if angle >= 500:
            angle -= 10
        car.turn_left(angle)
    elif keys_pressed['d']:
        if angle <= 2500:
            angle += 10
        car.turn_right(angle)
    if keys_pressed[' ']:
        car.reset_direction()

def server(car_port):
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
                    data = conn.recv(2).decode('ascii')
                    if not data:
                        break
                    # print(data)
                    key = data[0]
                    pressed = data[1] == '1'
                    if key in keys_pressed:
                        keys_pressed[key] = pressed
                        handle_keys()
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