
import RPi.GPIO as gp
import time

# gp.cleanup()
gp.setmode(gp.BCM)

gp.setup(18, gp.OUT)
servo = gp.PWM(18,50)
servo.start(2.0)

def rotation(angle):
    return 1.5 + angle / (180 / 11)


while True:
    #  1.5 ~ 12.5
    #  2 : 0 degree  ~ 12 : 180 degree
    for i in range(0,72):
        if i<36:
            servo.ChangeDutyCycle(rotation(5*i))
        else:
            servo.ChangeDutyCycle(rotation(360-5*i))
        time.sleep(0.008)
        # max speed : 5 degree / 0.008 sec at rpi 5v


