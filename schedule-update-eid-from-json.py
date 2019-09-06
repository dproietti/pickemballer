
from app import db, models, utils
import requests
import datetime

## the database field eid does not match nfl json
## use script to update eid field to match json

def getCurrentNFLWeek():
    dt = datetime.datetime.now()
    if dt.isocalendar()[2] in [4,5,6,7]:
        return dt.isocalendar()[1] - 35
    else:
        return dt.isocalendar()[1] - 36

week = getCurrentNFLWeek()

url = 'http://www.nfl.com/liveupdate/scores/scores.json'
print "Week: %s" % week
print "URL: %s" % url

r = requests.get(url)
jsonScores =  r.json()

dt = datetime.datetime.now()
dt = utils.convertUtcToEST()

for eid in jsonScores.keys():
    #print eid
    homeTeam = jsonScores[eid]['home']['abbr']
    awayTeam = jsonScores[eid]['away']['abbr']
    print "UPDATE schedule SET eid=%s WHERE week=%s and home_team='%s' and away_team='%s';" % (eid, week, homeTeam, awayTeam)
