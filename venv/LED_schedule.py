from gpiozero import PWMLED
from time import sleep

led = PWMLED(18)
led.value = 0
led.on()

while True:
    led.value += 0.01
    sleep(0.1)