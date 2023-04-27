from imuread import IMU
from time import sleep
import RPi.GPIO as gp

# gp.cleanup()
gp.setmode(gp.BCM)

gp.setup(18, gp.OUT)
servo = gp.PWM(18,50)
servo.start(2.0)

def rotation(angle):
    return 1.5 + angle / (180 / 11)

imuserial = IMU( port="/dev/ttyUSB0" )
imuserial.start()
imuserial.reading = True

while True:
    r = imuserial.roll
    print(r)
    if r > 180:
        r = 180
    if r < 0:
        r = 0
    servo.ChangeDutyCycle(rotation(r))
    sleep(0.008)
        # max speed : 5 degree / 0.008 sec at rpi 5v


