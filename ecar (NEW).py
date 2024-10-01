# NEW CODE:

    # class Car:

    #   def drive():
    #       drive_helper()
    #       start thread

    #   def drive_helper()
    #       while True:
    #           set left motor to speed
    #           set right motor to speed
    #           set servo angle
    #           small delay

    #   def stop():
    #       drive_thread.kill()

    #   def speed_set():
    #       manipulates both back motors

    #   def turn():
    #       angles servos and reduces one back motor

    #   def brake():
    #       set back motors to negeative very briefly and then to 0

    # class-wide/instance variables
    # 1. left speed
    # 2. right speed
    # 3. servo angle

    # use asyncio, which looks like:

    # async def drive():
    #   while True:
    #       ...
    #   await asyncio.sleep()

# first iteration:
'''
import asyncio, pigpio, time, keyboard, math

SERV_LIMIT = 45
SPD_LIMIT = 100

class Car:

    def __init__(self, rm_spd = 0, lm_spd = 0, serv_ang = 0):
        self.rm_spd = rm_spd
        self.lm_spd = lm_spd
        self.serv_ang = serv_ang

    def drive(self):
        self.drive_helper()

    async def drive_helper(self):
        while True:
            self.speed_set()
            self.turn()
            self.brake()
            await asyncio.sleep(0.001)

    async def speed_set(self, lm_spd, rm_spd):
        if keyboard.is_pressed('w'):
            lm_spd += 1
            rm_spd += 1
        elif keyboard.is_pressed('s'):
            lm_spd -= 1
            rm_spd -= 1

    async def brake(self, lm_spd, rm_spd):
        if keyboard.is_pressed('b'):
            lm_spd = -lm_spd
            rm_spd = -rm_spd
            await asyncio.sleep(0.1)
            lm_spd = 0
            rm_spd = 0

    async def turn(self, serv_angle, lm_spd, rm_spd):
        if keyboard.is_pressed('a'):
            serv_angle -= 1
            lm_spd -= rm_spd - math.sqrt(serv_angle)
        elif keyboard.is_pressed('d'):
            serv_angle += 1
            rm_spd -= lm_spd - math.sqrt(serv_angle)

    def stop(self):
        pass

def main():
    ecar = Car()
    ecar.drive()

if __name__ == "__main__":
    main()
'''

# after ChatGPT:
import asyncio, pigpio, keyboard

# Define GPIO pins for motors and servo
RIGHT_MOTOR_PIN = 17
LEFT_MOTOR_PIN = 18
SERVO_PIN = 27

SERV_LIMIT = 45  # Servo angle limit
SPD_LIMIT = 100  # Speed limit for motors (0-100)

class Car:
    def __init__(self, pi, rm_spd = 0, lm_spd = 0, serv_ang = 0):
        self.rm_spd = rm_spd
        self.lm_spd = lm_spd
        self.serv_ang = serv_ang
        self.pi = pi

        # Initialize pigpio motor and servo
        self.pi.set_mode(RIGHT_MOTOR_PIN, pigpio.OUTPUT)
        self.pi.set_mode(LEFT_MOTOR_PIN, pigpio.OUTPUT)
        self.pi.set_mode(SERVO_PIN, pigpio.OUTPUT)

    async def drive(self):
        while True:
            await self.speed_set()
            await self.turn()
            await self.brake()
            await asyncio.sleep(0.01)  # Run at a faster loop rate

    async def speed_set(self):
        # Increase speed with 'w', decrease with 's'
        if keyboard.is_pressed('w') and self.rm_spd < SPD_LIMIT:
            self.rm_spd += 1
            self.lm_spd += 1
        elif keyboard.is_pressed('s') and self.rm_spd > 0:
            self.rm_spd -= 1
            self.lm_spd -= 1

        # Update motor speeds using pigpio
        self.pi.set_PWM_dutycycle(RIGHT_MOTOR_PIN, self.rm_spd)
        self.pi.set_PWM_dutycycle(LEFT_MOTOR_PIN, self.lm_spd)

    async def brake(self):
        if keyboard.is_pressed('b'):
            self.rm_spd = 0
            self.lm_spd = 0
            # Stop motors
            self.pi.set_PWM_dutycycle(RIGHT_MOTOR_PIN, 0)
            self.pi.set_PWM_dutycycle(LEFT_MOTOR_PIN, 0)
            await asyncio.sleep(0.1)

    async def turn(self):
        # Adjust servo angle for turning
        if keyboard.is_pressed('a') and self.serv_ang > -SERV_LIMIT:
            self.serv_ang -= 1
        elif keyboard.is_pressed('d') and self.serv_ang < SERV_LIMIT:
            self.serv_ang += 1

        # Update servo angle
        pulsewidth = 1500 + (self.serv_ang * 10)  # Convert angle to pulsewidth
        self.pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth)

    def stop(self):
        # Stop all motors and reset servo
        self.pi.set_PWM_dutycycle(RIGHT_MOTOR_PIN, 0)
        self.pi.set_PWM_dutycycle(LEFT_MOTOR_PIN, 0)
        self.pi.set_servo_pulsewidth(SERVO_PIN, 1500)  # Reset to neutral

async def main():
    # Initialize pigpio daemon
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("Could not connect to pigpio daemon")

    car = Car(pi)
    try:
        await car.drive()
    except KeyboardInterrupt:
        car.stop()
    finally:
        pi.stop()  # Clean up pigpio resources

if __name__ == "__main__":
    asyncio.run(main())