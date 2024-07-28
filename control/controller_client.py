import socket
import sys
from pynput import keyboard
from pynput.keyboard import KeyCode, Key

class ControllerClient:
    def __init__(self, car_ip, car_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((car_ip, car_port))

    def send_data(self, data, pressed):
        data = (data + ('1' if pressed else '0')).encode('ascii')
        self.s.sendall(data)

def on_press(key, client):
    if key == Key.esc:
        sys.exit()
    elif key == Key.space:
        client.send_data(' ', True)
    elif key in [KeyCode.from_char('w'), KeyCode.from_char('a'), KeyCode.from_char('s'), KeyCode.from_char('d')]:
        client.send_data(key.char, True)

def on_release(key, client):
    if key == Key.space:
        client.send_data(' ', False)
    elif key in [KeyCode.from_char('w'), KeyCode.from_char('a'), KeyCode.from_char('s'), KeyCode.from_char('d')]:
        client.send_data(key.char, False)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: python controller_client.py [Car IP] [Car Port]")
    car_ip = sys.argv[1]
    car_port = int(sys.argv[2])
    client = ControllerClient(car_ip, car_port)
    listener = keyboard.Listener(
        on_press=lambda key: on_press(key, client),
        on_release=lambda key: on_release(key, client)
    )
    listener.start()
    listener.join()