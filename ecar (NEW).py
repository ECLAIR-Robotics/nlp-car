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

import asyncio, pigpio, time, keyboard

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
            lm_spd -= 1
        elif keyboard.is_pressed('d'):
            serv_angle += 1
            rm_spd -= 1

    def stop(self):
        pass