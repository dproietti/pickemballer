

import sys
import requests
import csv
import datetime
from app import db, models

def getCurrentNFLWeek():
    dt = datetime.datetime.now()
    if dt.isocalendar()[2] in [4,5,6,7]:
        return dt.isocalendar()[1] - 35
    else:
        return dt.isocalendar()[1] - 36

def addPointSpread(week, homeTeam, homeLine, awayLine, overUnder):
    game = models.Schedule.query.filter_by(week=week,home_team=homeTeam).first()                                                                          
    game.home_line = homeLine
    game.away_line = awayLine
    game.over_under = overUnder
    db.session.commit()

year = 2016
week = None

if len(sys.argv) >=2:
    week = sys.argv[1]
else:
    week = getCurrentNFLWeek()
    
url = "https://fantasysupercontest.com/nfl-export?year=%s&week=%s&format=csv" % (year, week)

print "Load Spread for week %s from %s" % (week, url)

with requests.Session() as s:
    download = s.get(url)
    decoded_content = download.content.decode('utf-8')
    input_file = csv.DictReader(decoded_content.splitlines(), delimiter=',')
    
    for row in input_file:
        if row['home_team'] == 'JAC':
            row['home_team'] = 'JAX'

        #print "home team: %s" % row['home_team']
        #print "home line: %s" % row['home_line']
        
        addPointSpread(week=row['week'],
            homeTeam =  row['home_team'], 
            homeLine = row['home_line'], 
            awayLine = row['away_line'], 
            overUnder = row['over_under']            )
