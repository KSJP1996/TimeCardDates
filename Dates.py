''' This program will generate an ics file for days to sign time cards
    will check if the 15 and last day of month to see if its a weekday
    or back trace to find to a Friday
'''
import datetime
from icalendar import Calendar, Event, Alarm
import calendar as basic_calendar
from datetime import timedelta
import pytz

def currentDay():
    ''' Gets the current year
    '''
    now = datetime.datetime.now()
    return(now.year, now)

def generateDatetime(edate, hour, minute, second):
    ''' Converts all of the seperate dates to single string
    '''
    event = datetime.datetime(edate.year, edate.month, edate.day, hour, minute, second)
    return event

def localize(utcTime):
    ''' localize the timezone to Centreal aka 'America/Chicago'
    '''
    timezone = pytz.timezone("America/Chicago")
    localizedDatetime = timezone.localize(utcTime)
    return localizedDatetime

def checkday(year, month, day):
    ''' Check the current date to see what dat it is
    '''
    check = datetime.date(year, month, day)
    checkDay = check.weekday() # monday = 0 , Sunday = 6
    # check if weekend
    if checkDay == 5 or 6 :
        checkDay = 4 # if the 15 or ldm falls on a weekend move to Friday

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

def generateEvent(cal, edate):
    ''' Generate a 10 minute long event once give an a date
    '''
    date = generateDatetime(edate, 14, 0, 0) # create event at 2:00 PM
    #date = localize(date) # locized by outlook(I think )
    endDate = date + timedelta(minutes=15)

    newEvent = Event()
    newEvent.add('summary',"Sign Time Card")
    newEvent.add('dtstart', date)
    newEvent.add('dtend', endDate)
    newEvent = addAlarm(newEvent)
    cal.add_component(newEvent)
    return cal

def addAlarm(event):
    ''' Add in an alarm to the event
    ''' 
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alert_time = timedelta(minutes=-int(5)) ## alert the user 5 minutes before 2:00 i.e. 1:55
    alarm.add('trigger', alert_time)
    event.add_component(alarm)
    return event

def main():
    ''' Actual Code
    '''
    [*_, now] = currentDay()
    cal = Calendar()
    cal = cycleYear(cal, now)

    myFile = open('TimeCard.ics', 'wb')
    myFile.write(cal.to_ical())
    myFile.close()

    print("ics generated")

if __name__ == '__main__':
    main()
