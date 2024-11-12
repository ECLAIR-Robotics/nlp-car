'''
# first iteration, no asyncio, uses turtle


import turtle, keyboard, time

POWER_LIMIT = 100
TURN_LIMIT = 45

class Car:

    def __init__(self, speed, angle):
        self.speed = speed
        self.angle = angle

    def set_speed(self, val):
        self.speed += val

    def set_turn_angle(self, val):
        self.angle += val

def drive():

    car = Car(0, 0)

    drive = True
    while drive:

        if keyboard.is_pressed('w'):
            if car.speed < POWER_LIMIT:
                car.set_speed(1)
        elif keyboard.is_pressed('s'):
            if car.speed > -POWER_LIMIT:
                car.set_speed(-1)
        turtle.forward(car.speed)
    
        if keyboard.is_pressed('a'):
            if car.angle > -TURN_LIMIT:
                car.set_turn_angle(-1)
        elif keyboard.is_pressed('d'):
            if car.angle < TURN_LIMIT:
                car.set_turn_angle(1)
        turtle.right(car.angle)

        time.sleep(0.001)

    turtle.done()

drive()
'''

'''
# second iteration, asyncio added

import turtle, keyboard, asyncio

POWER_LIMIT = 10
TURN_LIMIT = 30

class Car:

    def __init__(self, speed, angle):
        self.speed = speed
        self.angle = angle

    async def set_speed(self, val):
        self.speed += val
        print(f'Current Speed: {self.speed}')

    async def set_turn_angle(self, val):
        self.angle += val
        print(f'Current Angle: {self.angle}')

async def main():

    car = Car(0, 0)

    drive = True
    while drive:

        if keyboard.is_pressed('w'):
            if car.speed < POWER_LIMIT:
                await car.set_speed(1)
        elif keyboard.is_pressed('s'):
            if car.speed > -POWER_LIMIT:
                await car.set_speed(-1)
        turtle.forward(car.speed)
    
        if keyboard.is_pressed('a'):
            if car.angle > -TURN_LIMIT:
                await car.set_turn_angle(-1)
        elif keyboard.is_pressed('d'):
            if car.angle < TURN_LIMIT:
                await car.set_turn_angle(1)
        turtle.right(car.angle)

    turtle.done()

if __name__ == '__main__':
    asyncio.run(main())
'''

# second iteration, asyncio added

import turtle
import keyboard
import asyncio

POWER_LIMIT = 10
TURN_LIMIT = 30

class Car:

    def __init__(self, speed, angle):
        self.speed = speed
        self.angle = angle

    async def set_speed(self, val):
        self.speed += val
        print(f'Current Speed: {self.speed}')

    async def set_turn_angle(self, val):
        self.angle += val
        print(f'Current Angle: {self.angle}')

async def fibonacci():
    num1 = 0
    num2 = 1
    next_num = num2  
    while True:
        await asyncio.sleep(1)
        print(f'FibSeq: {next_num}')
        num1, num2 = num2, next_num
        next_num = num1 + num2

async def control_car(car):

    while True:
        if keyboard.is_pressed('w'):
            if car.speed < POWER_LIMIT:
                await car.set_speed(1)
        elif keyboard.is_pressed('s'):
            if car.speed > -POWER_LIMIT:
                await car.set_speed(-1)

        if keyboard.is_pressed('a'):
            if car.angle > -TURN_LIMIT:
                await car.set_turn_angle(-1)
        elif keyboard.is_pressed('d'):
            if car.angle < TURN_LIMIT:
                await car.set_turn_angle(1)

        turtle.forward(car.speed)
        turtle.right(car.angle)

        await asyncio.sleep(0.02) 

async def main():
    car = Car(0, 0)

    await asyncio.gather(
        control_car(car),
        fibonacci()
    )

if __name__ == '__main__':
    asyncio.run(main())
