import datetime
import calendar as basic_calendar
from datetime import timedelta
from ics import Calendar, Event
from pytz import UTC #Timezone

def currentDay():
    ''' Gets the current year
    '''
    now = datetime.datetime.now()
    return(now.year, now)

def generateDatetime(edate, hour, minute, second):
    ''' Converts all of the seperate dates to single string
    '''
    event = datetime.datetime(edate.year, edate.month, edate.day, hour, minute, second, tzinfo=UTC)
    return event

def generateEvent(cal, edate):
    ''' Generate a 10 minute long event once give an a date
    '''
    newEvent = Event()
    newEvent.name = "Sign Time Card"
    date = generateDatetime(edate, 14, 0, 0) # create event at 2:00 PM
    date = date + timedelta(hours=5) # ics is 5 hours off
    newEvent.begin = date
    newEvent.end = date + timedelta(minutes=15)
    cal.events.add(newEvent)
    #cal.events # make the event
    return cal

def checkday(y, m, d):
    ''' Check the current date to see what dat it is
    '''
    check = datetime.date(y, m, d)
    dayName = check.weekday() # monday = 0 , Sunday = 6
    # check if weekend
    if dayName == 5:
        d -= 1
    if dayName == 6:
        d -= 2
    return [y, m, d]

def cycleYear(cal, now):
    ''' Check the 15th and last day of the month to see if it is a weekday else it will back count
        till a weekday is found
    '''
    cYear = now.year
    cMonth = now.month

    while cMonth < 13:
        # check the 15
        [gy, gm, gd] = checkday(cYear, cMonth, 15)# test the 15th
        date = datetime.date(gy, gm, gd)
        cal = GenerateEvent(cal, date) # write the event

        # check the last day of the month aka ldm
        [__, lDM] = basic_calendar.monthrange(cYear, cMonth) #get last of the month
        [gy, gm, gd] = checkday(cYear, cMonth, lDM)
        date = datetime.date(gy, gm, gd)
        cal = GenerateEvent(cal, date)# write the event
        cMonth += 1 # increment month by 1
    return cal

def main():
    ''' Actual Code
    '''
    [__, now] = currentDay()
    cal = Calendar()
    caln = cycleYear(cal, now)

    with open('TimeCard.ics', 'w') as myFile:
        myFile.writelines(caln)
    print("ics generated")

if __name__ == '__main__':
    main()
