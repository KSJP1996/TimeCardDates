''' This program will generate an ics file for days to sign time cards
    will check if the 15 and last day of month to see if its a weekday
    or back trace to find to a Friday
'''
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

def checkday(year, month, day):
    ''' Check the current date to see what dat it is
    '''
    check = datetime.date(year, month, day)
    checkDay = check.weekday() # monday = 0 , Sunday = 6
    # check if weekend
    if checkDay == 5:
        day -= 1
    if checkDay == 6:
        day -= 2
    return [year, month, day]

def cycleYear(cal, now):
    ''' Check the 15th and last day of the month to see if it is a weekday else it will back count
        till a weekday is found
    '''
    cYear = now.year
    cMonth = now.month
    while cMonth < 13:
        # check the 15
        [getYear, getMonth, getDay] = checkday(cYear, cMonth, 15)# test the 15th
        date = datetime.date(getYear, getMonth, getDay)
        cal = generateEvent(cal, date) # write the event

        # check the last day of the month aka ldm
        [*_, lDM] = basic_calendar.monthrange(cYear, cMonth) #get last of the month
        [getYear, getMonth, getDay] = checkday(cYear, cMonth, lDM)
        date = datetime.date(getYear, getMonth, getDay)
        cal = generateEvent(cal, date)# write the event
        cMonth += 1 # increment month by 1
    return cal

def main():
    ''' Actual Code
    '''
    [*_, now] = currentDay()
    cal = Calendar()
    caln = cycleYear(cal, now)

    with open('TimeCard.ics', 'w') as myFile:
        myFile.writelines(caln)
    print("ics generated")

if __name__ == '__main__':
    main()
