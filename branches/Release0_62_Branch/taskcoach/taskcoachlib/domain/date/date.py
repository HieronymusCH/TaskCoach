import patterns
import time, string, datetime, timedelta

infinite = datetime.date.max
minimumDate = datetime.date.min
    
class RealDate(datetime.date):

    def __init__(self, year, month, day):
        super(RealDate, self).__init__(year, month, day)

    def weekday(self):
        return self.isoweekday()

    def weeknumber(self):
        return self.isocalendar()[1]

    def nextWeekday(self, weekday):
        result = self
        while result.weekday() != weekday:
            result = result + timedelta.oneDay
        return result

    def nextSunday(self):
        return self.nextWeekday(7)

    def nextFriday(self):
        return self.nextWeekday(5)
        
    def __add__(self, delta):
        newdate = super(RealDate, self).__add__(delta)
        return RealDate(newdate.year, newdate.month, newdate.day)

    def __sub__(self, other):
        newdate = super(RealDate, self).__sub__(other)
        if isinstance(newdate, datetime.timedelta):
            return timedelta.TimeDelta(newdate.days, newdate.seconds, newdate.microseconds)
        else:
            return RealDate(newdate.year, newdate.month, newdate.day)


class InfiniteDate(datetime.date):
    __metaclass__ = patterns.Singleton

    def __new__(self):
        return super(InfiniteDate, self).__new__(InfiniteDate, infinite.year,
            infinite.month, infinite.day)

    def _getyear(self):
        return None

    year = property(_getyear)

    def _getmonth(self):
        return None

    month = property(_getmonth)

    def _getday(self):
        return None

    day = property(_getday)

    def __str__(self):
        return 'None'

    def weekday(self):
        return None

    def weeknumber(self):
        return None

    def __sub__(self, other):
        if isinstance(other, InfiniteDate):
            return timedelta.TimeDelta()
        else:
            return timedelta.TimeDelta.max

# factories:

def parseDate(dateString, default=None):
    try:
        return Date(*[string.atoi(part) for part in dateString.split('-')])
    except ValueError:
        if default:
            return default
        else:
            return Date()

def Date(year=infinite.year, month=infinite.month, day=infinite.day):
    if (year, month, day) == (infinite.year, infinite.month, infinite.day):
        return InfiniteDate()
    else:
        return RealDate(year, month, day)

def Today():
    today = datetime.date.today()
    return RealDate(today.year, today.month, today.day)

def Tomorrow():
    tomorrow = datetime.date.today() + timedelta.oneDay
    return RealDate(tomorrow.year, tomorrow.month, tomorrow.day)

def Yesterday():
    yesterday = datetime.date.today() - timedelta.oneDay
    return RealDate(yesterday.year, yesterday.month, yesterday.day)

def NextSunday():
    return Today().nextSunday()

def NextFriday():
    return Today().nextFriday()

def LastDayOfCurrentMonth(localtime=time.localtime):
    now = localtime()
    year, nextMonth = now[0], now[1]+1
    if nextMonth > 12:
        nextMonth = 1
        year += 1
    return Date(year, nextMonth, 1) - timedelta.oneDay 

def LastDayOfCurrentYear():
    now = time.localtime()
    return Date(now[0], 12, 31)
