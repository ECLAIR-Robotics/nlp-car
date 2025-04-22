import pigpio

class Car:
    def __init__(self, servo_pin, motor1_pins, motor2_pins) -> None:
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise Exception("Could not connect to pigpio daemon")

        self.servo_pin = servo_pin
        self.motor1_pins = motor1_pins
        self.motor2_pins = motor2_pins

        self.pi.set_mode(servo_pin, pigpio.OUTPUT)
        self.pi.set_mode(motor1_pins[0], pigpio.OUTPUT)
        self.pi.set_mode(motor1_pins[1], pigpio.OUTPUT)
        self.pi.set_mode(motor2_pins[0], pigpio.OUTPUT)
        self.pi.set_mode(motor2_pins[1], pigpio.OUTPUT)

        self.pi.set_PWM_frequency(servo_pin, 50)
        self.pi.set_PWM_frequency(motor1_pins[0], 50)
        self.pi.set_PWM_frequency(motor1_pins[1], 50)
        self.pi.set_PWM_frequency(motor2_pins[0], 50)
        self.pi.set_PWM_frequency(motor2_pins[1], 50)

    def forward(self, speed):
        duty_cycle = int(speed * 255 / 100)
        self.pi.set_PWM_dutycycle(self.motor1_pins[0], duty_cycle)
        self.pi.set_PWM_dutycycle(self.motor1_pins[1], 0)
        self.pi.set_PWM_dutycycle(self.motor2_pins[0], duty_cycle)
        self.pi.set_PWM_dutycycle(self.motor2_pins[1], 0)

    def reverse(self, speed):
        duty_cycle = int(speed * 255 / 100)
        self.pi.set_PWM_dutycycle(self.motor1_pins[0], 0)
        self.pi.set_PWM_dutycycle(self.motor1_pins[1], duty_cycle)
        self.pi.set_PWM_dutycycle(self.motor2_pins[0], 0)
        self.pi.set_PWM_dutycycle(self.motor2_pins[1], duty_cycle)

    def turn_left(self, angle):
        self.pi.set_servo_pulsewidth(self.servo_pin, angle)
    
    def turn_right(self, angle): 
        self.pi.set_servo_pulsewidth(self.servo_pin, angle)

    def brake(self):
        self.pi.set_PWM_dutycycle(self.motor1_pins[0], 0)
        self.pi.set_PWM_dutycycle(self.motor1_pins[1], 0)
        self.pi.set_PWM_dutycycle(self.motor2_pins[0], 0)
        self.pi.set_PWM_dutycycle(self.motor2_pins[1], 0)

    def stop(self):
        self.brake()
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)

    def reset_direction(self):
        # Tune this value if car starts to drift
        self.pi.set_servo_pulsewidth(self.servo_pin, 1500)

    def cleanup(self):
        self.pi.stop()