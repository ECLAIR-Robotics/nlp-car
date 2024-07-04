import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard

class Car:
    def __init__(self, servo_pin, motor1_pins, motor2_pins) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        GPIO.setup(motor1_pins[0], GPIO.OUT)
        GPIO.setup(motor1_pins[1], GPIO.OUT)
        GPIO.setup(motor2_pins[0], GPIO.OUT)
        GPIO.setup(motor2_pins[1], GPIO.OUT)

        self.servo = GPIO.PWM(servo_pin, 50)
        self.motor1 = [GPIO.PWM(motor1_pins[0], 50), GPIO.PWM(motor1_pins[1], 50)]
        self.motor2 = [GPIO.PWM(motor2_pins[0], 50), GPIO.PWM(motor2_pins[1], 50)]
        
        self.servo.start(0)
        self.motor1[0].start(0)
        self.motor1[1].start(0)
        self.motor2[0].start(0)
        self.motor2[1].start(0)

    def forward(self, speed=50):
        self.motor1[0].ChangeDutyCycle(speed)
        self.motor1[1].ChangeDutyCycle(0)
        self.motor2[0].ChangeDutyCycle(speed)
        self.motor2[1].ChangeDutyCycle(0)

    def reverse(self, speed=50):
        self.motor1[0].ChangeDutyCycle(0)
        self.motor1[1].ChangeDutyCycle(speed)
        self.motor2[0].ChangeDutyCycle(0)
        self.motor2[1].ChangeDutyCycle(speed)

    def turn_left(self):
        self.servo.ChangeDutyCycle(20)
    
    def turn_right(self): 
        self.servo.ChangeDutyCycle(1)

    def brake(self):
        self.motor1[0].ChangeDutyCycle(0)
        self.motor1[1].ChangeDutyCycle(0)
        self.motor2[0].ChangeDutyCycle(0)
        self.motor2[1].ChangeDutyCycle(0)

    def stop(self):
        self.brake()
        self.servo.stop()

    def reset_direction(self):
        self.servo.ChangeDutyCycle(8.5)
        # self.servo.ChangeDutyCycle(0)

class Controller:
    def __init__(self):
        servo_pin = 21
        motor1_pins = [27, 17]
        motor2_pins = [23, 24]

        self.car = Car(servo_pin, motor1_pins, motor2_pins)
        self.start()

    def start(self):
        listen_keyboard(
            on_press=self.press_key,
            on_release=self.release_key,
        )

    def press_key(self, key):
        if key == 'w':
            self.car.forward(50)
        elif key == 's':
            self.car.reverse(50)
        elif key == 'a':
            self.car.turn_left()
        elif key == 'd':
            self.car.turn_right()
        elif key == 'space':
            self.car.brake()

    def release_key(self, key):
        if key in ['a', 'd']:
            self.car.reset_direction()
        # elif key in ['w', 's']:
        #     self.car.brake()
        

def main():
    controller = Controller()
    controller.start()

if __name__ == '__main__':
    main()