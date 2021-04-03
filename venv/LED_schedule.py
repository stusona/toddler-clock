from gpiozero import PWMLED
from time import sleep
import datetime
import pytz

green_led = PWMLED(18) # green LED GPIO number
green_led.value = 0
TARGET_HOUR = 20
TARGET_MINUTE = 12

utc = pytz.utc
pst = pytz.timezone('America/Los_Angeles')

fmt = '%Y-%m-%d %H:%M:%S'

while True:
	utc_dt = datetime.datetime.now().replace(tzinfo=utc)
	print(f"UTC time: {utc_dt.striftime(fmt)}")
	pst_dt = utc_dt.astimezone(pst)
	print("PST time: {}".format(pst_dt.strftime(fmt)))

	target_time = pst_dt.replace(hour=TARGET_HOUR, minute=TARGET_MINUTE)
	if(pst_dt < target_time):
		print("Waiting")
		countdown = target_time - pst_dt
		print(countdown.seconds)

	green_led.value = (green_led.value + 0.05) % 1
	print("\n")
	sleep(2)
