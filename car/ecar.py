import pigpio

SERVO_MIN = 500
SERVO_RST = 1500
SERVO_MAX = 2500

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

    def accel(self, speed):
        duty_cycle = int(abs(speed) * 255 / 100)
        if speed > 0:       # forward
            self.pi.set_PWM_dutycycle(self.motor1_pins[0], duty_cycle)
            self.pi.set_PWM_dutycycle(self.motor1_pins[1], 0)
            self.pi.set_PWM_dutycycle(self.motor2_pins[0], duty_cycle)
            self.pi.set_PWM_dutycycle(self.motor2_pins[1], 0)
        elif speed < 0:     # reverse
            self.pi.set_PWM_dutycycle(self.motor1_pins[0], 0)
            self.pi.set_PWM_dutycycle(self.motor1_pins[1], duty_cycle)
            self.pi.set_PWM_dutycycle(self.motor2_pins[0], 0)
            self.pi.set_PWM_dutycycle(self.motor2_pins[1], duty_cycle)
        else:
            self.brake()

    def turn(self, strength):
        if strength > 0:    # turn left
            pulsewidth = strength / 100 * (SERVO_MAX - SERVO_RST) + SERVO_RST
        elif strength < 0:  # turn right
            pulsewidth = SERVO_RST + strength / 100 * (SERVO_RST - SERVO_MIN)
        else:
            pulsewidth = SERVO_RST
        self.pi.set_servo_pulsewidth(self.servo_pin, pulsewidth)
    
    def brake(self):
        self.pi.set_PWM_dutycycle(self.motor1_pins[0], 0)
        self.pi.set_PWM_dutycycle(self.motor1_pins[1], 0)
        self.pi.set_PWM_dutycycle(self.motor2_pins[0], 0)
        self.pi.set_PWM_dutycycle(self.motor2_pins[1], 0)

    def stop(self):
        self.brake()
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
    
    def cleanup(self):
        self.pi.stop()