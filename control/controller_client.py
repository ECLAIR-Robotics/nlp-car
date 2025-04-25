import socket
import sys
import threading
import time
from pynput import keyboard
from pynput.keyboard import KeyCode, Key
from pynput import mouse
import pyautogui

pyautogui.FAILSAFE = False

class ControllerClient:
    def __init__(self, car_ip, car_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((car_ip, car_port))

    def send_data(self, data, pressed=True):
        if data.startswith(('x', 'y')):
            msg = data.encode('ascii')
        self.s.sendall(msg)

mouse_x = 0
mouse_y = 0
last_move_time = time.time()
move_timer = None
mouse_lock = threading.Lock()

screen_size = pyautogui.size()
screen_width = screen_size.width
screen_height = screen_size.height
center_x = screen_width // 2
center_y = screen_height // 2

def on_click():
    stop_event.set()
    mouse_listener.stop()
    sys.exit()

def on_mouse_move(x, y):
    global mouse_x, mouse_y, last_move_time, move_timer
    with mouse_lock:
        mouse_x = int(x)
        mouse_y = int(y)
        last_move_time = time.time()
    if move_timer:
        move_timer.cancel()
    move_timer = threading.Timer(0.05, recenter_mouse_if_idle)
    move_timer.start()

def recenter_mouse_if_idle():
    global last_move_time, mouse_x, mouse_y
    if time.time() - last_move_time >= 0.05 and not stop_event.is_set():
        pyautogui.moveTo(center_x, center_y)
        with mouse_lock:
            mouse_x = center_x
            mouse_y = center_y

def send_mouse_periodically(client, interval=0.1):
    global mouse_x, mouse_y
    while not stop_event.is_set():
        time.sleep(interval)
        with mouse_lock:
            turn_percent = int(((mouse_x / screen_width) - 0.5) * 200)
            turn_percent = max(-100, min(100, turn_percent))

            speed_percent = -int(((mouse_y / screen_height) - 0.5) * 200)
            speed_percent = max(-100, min(100, speed_percent))

        client.send_data(f'x{turn_percent}')
        client.send_data(f'y{speed_percent}')
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: python controller_client.py [Car IP] [Car Port]")
    car_ip = sys.argv[1]
    car_port = int(sys.argv[2])
    client = ControllerClient(car_ip, car_port)

    stop_event = threading.Event()

    mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_click)
    mouse_thread = threading.Thread(target=send_mouse_periodically, args=(client,), daemon=True)

    mouse_listener.start()
    mouse_thread.start()

    mouse_listener.join()
    mouse_thread.join()
