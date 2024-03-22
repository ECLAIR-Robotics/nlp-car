
from time import sleep

from machine import Pin

from machine import PWM

class Servo:
    
    # create a new servo
    def __init__(self):
        pwm = PWM(Pin(0))
        pwm.freq(50)

    
    # helper function for moving the servo
    def setServoCycle (position):
        pwm.duty_u16(position)
        sleep(0.01)

    # move servo motor forward 180 degrees
    def forward:
        for pos in range(1000,9000,50):
            setServoCycle(pos)

    # move servo motor backward 180 degrees
    def backward:
        for pos in range(9000,1000,-50):
            setServoCycle(pos)

    # turn servo motor x degrees right
    def turn_right:
        #help idk

    # turn servo motor x degrees left
    def turn_left:
