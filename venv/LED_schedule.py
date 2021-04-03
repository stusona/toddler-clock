# Clock for a toddler:
# Strip of LEDs are red all night, then slowly turn green as a set time is
# approached so the little one knows it's ok to go in mom and dad's room

# Stuart Sonatina 2021

import neopixel
import board
from time import sleep
import datetime
import pytz

led_pin = board.D18 # LED GPIO number
led_num = 15 # number of LEDs
led_pow = 0.05 # 0-1 power for LEDs
ORDER = neopixel.GRB
ledstrip = neopixel.NeoPixel(
	led_pin, led_num, brightness=led_pow, auto_write=True, pixel_order=ORDER
)

red = (255,0,0)
grn = (0,255,0)
blu = (0,0,255)

ALARM_HOUR = 20; ALARM_MINUTE = 12 # time when the clock hits "zero" each morning
COUNTDOWN_TIME = 30 # Number of minutes to countdown

utc = pytz.utc # convenient timezone
pst = pytz.timezone('America/Los_Angeles')
fmt = '%Y-%m-%d %H:%M:%S' # format for printing timestamp

while True:
	utc_dt = datetime.datetime.now().replace(tzinfo=utc) # get current time
	print(f"UTC time: {utc_dt.striftime(fmt)}")
	pst_dt = utc_dt.astimezone(pst) # convert time to PST
	print("PST time: {}".format(pst_dt.strftime(fmt)))

	target_time = pst_dt.replace(hour=ALARM_HOUR, minute=ALARM_MINUTE)
	if(pst_dt < target_time):
		print("Waiting")
		countdown = target_time - pst_dt
		print(countdown.seconds)
		ledstrip.fill(red)
	else:
		ledstrip.fill(blu)
	sleep(2)
