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
import numpy

sleep_time = 1

MORNING_HOUR = 17; MORNING_MINUTE = 30 # time when the clock hits "zero" each morning
BEDTIME_HOUR = 20; BEDTIME_MINUTE = 15 # time when clock goes back to red
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
yel = (255,255,0)

tz = pytz.timezone('America/Los_Angeles')
utc = tz.localize(datetime.datetime.now()) # get current time
morning_time = utc.replace(hour=MORNING_HOUR, minute=MORNING_MINUTE, second=0)
bed_time = utc.replace(hour=BEDTIME_HOUR, minute=BEDTIME_MINUTE, second=0)
fmt = '%Y-%m-%d %H:%M:%S' # format for printing timestamp

def main():
    try:
        while True:
            dt = tz.localize(datetime.datetime.now()) # get current time
            print("Current time: {}".format(dt.strftime(fmt)))

            if(dt < morning_time): # Before morning alarm
                seconds_left = (morning_time - dt).total_seconds()
                if(seconds_left<COUNTDOWN_TIME): # we're in countdown mode
                    LED_countdown(red, grn, seconds_left)
                    print("LEDs are transitioning from red to green")
                else:
                    print("LEDs are red") # it's after midnight, but before countdown mode
                    ledstrip.fill(red)
                    ledstrip.show()

            elif(dt < bed_time): # it's after morning, but not bedtime yet
                seconds_left = (bed_time - dt).total_seconds()
                if(seconds_left<COUNTDOWN_TIME): # we're in countdown mode
                    LED_countdown(blu, red, seconds_left)
                    print("LEDs are transitioning from blue to red")
                else: # it's after morning, but not bedtime countdown yet
                    ledstrip.fill(blu)
                    ledstrip.show()
            else: # it's after bedtime, but before midnight
                ledstrip.fill(red)
                ledstrip.show()
            sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt")
        LED_off()

def LED_countdown(color_old, color_new, seconds_left):
    # take in old color, new color, and seconds left in countdown
    # set colors for all LEDs on strip
    new_leds_float = (1.0-(seconds_left/COUNTDOWN_TIME))*led_num
    transition = new_leds_float - int(new_leds_float) # Balance of old to new color in transition LED (0-1)
    new_led_count = int(new_leds_float) # Number of LEDs to color new color

    for i in range(new_led_count): # set new color for LEDs up to transition point
        ledstrip[i] = color_new

    trans_old = tuple(numpy.multiply((1-transition), color_old))
    trans_new = tuple(numpy.multiply(transition, color_old))
    color = numpy.add(trans_old, trans_new)
    ledstrip[new_led_count] = (int(color[0]), int(color[1]), int(color[2]))

    # ensure rest of strip is still old color
    for i in range(new_led_count,led_num):
        ledstrip[i]= color_old
    ledstrip.show()

def LED_off():
    ledstrip.fill((0,0,0))
    ledstrip.show()

if __name__ == '__main__':
    main()
