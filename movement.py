import RPi.GPIO as GPIO

class Movement:
    def __init__(self, servo_pin, motor1_pins, motor2_pins) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        GPIO.setup(motor1_pins[0], GPIO.OUT)
        GPIO.setup(motor1_pins[1], GPIO.OUT)
        GPIO.setup(motor2_pins[0], GPIO.OUT)
        GPIO.setup(motor2_pins[1], GPIO.OUT)

        self.servo = GPIO.PWM(servo_pin, 50)
        self.motor1 = [GPIO.PWM(motor1_pins[0], 50), GPIO.PWM(motor1_pins[1], 50)]
        self.motor2_pin2 = [GPIO.PWM(motor2_pins[0], 50), GPIO.PWM(motor2_pins[1], 50)]
        
        self.servo.start(0)
        self.motor1[0].start(0)
        self.motor1[1].start(0)
        self.motor2[0].start(0)
        self.motor2[1].start(0)

if __name__ == '__main__':
    pass