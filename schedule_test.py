import time
import schedule

def test_job():
    print("it's time!")

schedule.every().saturday.at("21:17").do(test_job)

while True:
        schedule.run_pending()
        time.sleep(1)
