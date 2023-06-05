import datetime

intervals = {
    "w": datetime.timedelta(weeks=1),
    "d": datetime.timedelta(days=1),
    "h": datetime.timedelta(hours=1),
    "m": datetime.timedelta(minutes=1),
    "s": datetime.timedelta(seconds=1),
}

def __pull_date_tuple(date_string):
    time_interval_start_index = 0
    date_string = date_string.strip()
    for char in date_string:
        if char.isnumeric():
            time_interval_start_index += 1
        else:
            return int(date_string[0:time_interval_start_index]), date_string[time_interval_start_index:]

    return False
    
def parse_live_date(date_string):
    date_interval = __pull_date_tuple(date_string)
    # "2w" used as an example
    if date_interval: 
        time_scalar, ll_interval = date_interval
        print(ll_interval)
        for interval in intervals:
            if interval == ll_interval:
                new_delta = time_scalar * intervals[interval]
                break 

        # Example of how it could be used
        current = datetime.datetime.now()
        new_time = current - new_delta
        print(new_time.day, new_time.month, new_time.year)
            

from parse_live_date import *       
parse_live_date('1d')
