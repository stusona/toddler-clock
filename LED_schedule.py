# Clock for a toddler:
# Strip of LEDs are red all night, then slowly turn green as a set time is
# approached so the little one knows it's ok to go in mom and dad's room

# Stuart Sonatina 2021

import neopixel
import board
from time import sleep
import schedule
import threading


#MORNING_TIME = "06:30" # time to start counting down each morning
MORNING_TIME = "06:00" # time to start counting down each morning
WAKEUP_TIME = "06:30" # time to turn blue
BED_TIME = "18:45" # time when clock goes back to red
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

def main():
    try:
        ledstrip.fill(red)
        ledstrip.show()
        print("LEDs red")
        schedule.every().day.at(MORNING_TIME).do(run_threaded, morning_countdown)
        schedule.every().day.at(WAKEUP_TIME).do(LED_blu)
        schedule.every().day.at(BED_TIME).do(run_threaded, bedtime_countdown)

        while True:
            schedule.run_pending()
            sleep(1)

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt, LEDs off")
        LED_off()

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def morning_countdown():
    LED_countdown(red, grn, COUNTDOWN_TIME, led_num)

def bedtime_countdown():
    LED_countdown(blu, red, COUNTDOWN_TIME, led_num)

def LED_countdown(color_old, color_new, seconds, led_num):
    # take in old color, new color, and seconds to do countdown
    # set colors for all LEDs on strip

    # ensure rest of strip is still old color
    ledstrip.fill(color_old)

    time_interval = seconds/led_num
    for i in range(led_num):
        sleep(time_interval)
        ledstrip[i] = color_new
        ledstrip.show()

def LED_blu():
    ledstrip.fill(blu)
    ledstrip.show()

def LED_off():
    ledstrip.fill((0,0,0))
    ledstrip.show()

if __name__ == '__main__':
    main()
