#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone


print('Date range engagement stats: A to B days ago (eg. 30 to 60 days ago)')
t1 = int(input("Enter A: "))
t2 = int(input("Enter B: "))


today = datetime.now(timezone.utc)
t1ago = today - timedelta(days=t1) 
t2ago = today - timedelta(days=t2)
format_data = "%Y-%m-%d %H:%M:%S %Z"
#example: 2024-12-15 13:25:17 UTC

with open('fan_daily_engagement_events.csv') as file:
    # i = 0
    openct = 0
    clickct = 0
    for line in file:
        # if i>10:
        #    break
        cols = line.split(',')
        try:
              eventdate = datetime.strptime(cols[3].strip(), format_data) #not an tz aware date
              if eventdate.tzinfo is None:
                 eventdate = eventdate.replace(tzinfo=timezone.utc)       #make tz aware
              if t2ago < eventdate < t1ago:                                   #check if date is within 20 days
                 if cols[2] == 'open':
                     openct += 1
                 elif cols[2] == 'click':
                     clickct += 1
        except ValueError:                                                #most likely a header row
              pass

        # i += 1
    
    print('Open count:', openct)
    print('Click count:', clickct)