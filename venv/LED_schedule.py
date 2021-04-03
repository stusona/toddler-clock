# Clock for a toddler:
# Strip of LEDs are red all night, then slowly turn green as a set time is
# approached so the little one knows it's ok to go in mom and dad's room

# Stuart Sonatina 2021

import neopixel
import board
from time import sleep
import datetime
import pytz
import tzlocal

sleep_time = 1

ALARM_HOUR = 06; ALARM_MINUTE = 30 # time when the clock hits "zero" each morning
COUNTDOWN_TIME = 30*60 # Number of seconds to count down and change LEDs

led_pow = 0.03 # 0-1 power for LEDs
led_pin = board.D18 # LED GPIO number
led_num = 15 # number of LEDs
ORDER = neopixel.GRB
ledstrip = neopixel.NeoPixel(
	led_pin, led_num, brightness=led_pow, auto_write=False, pixel_order=ORDER
)

red = (255,0,0)
grn = (0,255,0)
blu = (0,0,255)

tz = pytz.timezone('America/Los_Angeles')
dt = tz.localize(datetime.datetime.now()) # get current time
target_time = dt.replace(hour=ALARM_HOUR, minute=ALARM_MINUTE, second=0)
fmt = '%Y-%m-%d %H:%M:%S' # format for printing timestamp

while True:
    dt = tz.localize(datetime.datetime.now()) # get current time
    print("Current time: {}".format(dt.strftime(fmt)))

    if(dt < target_time):
        print("Waiting")
        countdown = (target_time - dt).total_seconds()
        print(countdown)
        ledstrip.fill(red)
        if(countdown<COUNTDOWN_TIME):
            green_leds = (1.0-(countdown/COUNTDOWN_TIME))*led_num
            trans_percentage = green_leds - int(green_leds)
            green_leds = int(green_leds)
            print(green_leds)
            for i in range(green_leds):
                ledstrip[i] = grn
            trans_grn = int(255*trans_percentage)
            print(f"trans_grn: {trans_grn}")
            trans_red = int(255*(1-trans_percentage))
            print(f"trans_red: {trans_red}")
            ledstrip[green_leds] = (trans_red, trans_grn, 0)
            ledstrip.show()
    else:
        ledstrip.fill(blu)
    sleep(sleep_time)
