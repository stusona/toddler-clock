from datetime import datetime, time, timedelta

def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

start_str = '0030'
end_str = '0050'

start_dt = datetime.strptime(start_str,"%H%M")
end_dt = datetime.strptime(end_str,"%H%M")

print(start_dt.time())

diff = (end_dt-start_dt)
print(diff.total_seconds()/60)
#print(time_in_range(start, end, current))

#print(current.strftime("%HH:%MM"))
# True (if you're not a night owl) ;)
morning = "06:30"
#print(int(morning.split(":")[0]))
