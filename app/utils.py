
import datetime
from pytz import timezone

from app import db, models
from .models import Team





def startTimeOfFirstGame(week):
    weeks = [u'2016-09-08 20:30:00', u'2016-09-15 20:25:00', u'2016-09-22 20:25:00', u'2016-09-29 20:25:00', u'2016-10-06 20:25:00', u'2016-10-13 20:25:00', u'2016-10-20 20:25:00', u'2016-10-27 20:25:00', u'2016-11-03 20:25:00', u'2016-11-10 20:25:00', u'2016-11-17 20:25:00', u'2016-11-24 12:30:00', u'2016-12-01 20:25:00', u'2016-12-08 20:25:00', u'2016-12-15 20:25:00', u'2016-12-22 20:25:00', u'2017-01-01 13:00:00']
    
    gameTime = datetime.datetime.strptime( weeks[week-1], "%Y-%m-%d %X" )
    EST=timezone('US/Eastern')
    return datetime.datetime(year=gameTime.year, month=gameTime.month, day=gameTime.day, hour=gameTime.hour, minute=gameTime.minute, second=gameTime.second, microsecond=111111, tzinfo=EST)
    #print weeks[week-1]
    #return  datetime.datetime.strptime( weeks[week-1], "%Y-%m-%d %X" )


def getTeams():
    teams = {}
    for team in Team.query.all():
        teams[team.id] = team
    return teams

def getCurrentNFLWeek():
    dt = datetime.datetime.now()
    if dt.isocalendar()[2] in [4,5,6,7]:
        return dt.isocalendar()[1] - 35
    else:
        return dt.isocalendar()[1] - 36

def convertUtcToEST(dt=None):
    EST=timezone('US/Eastern')
    if dt is None:
        dt = datetime.datetime.now(EST)
    
    return  datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute, second=dt.second, microsecond=000000, tzinfo=EST)