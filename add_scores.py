
from app import db, models
import requests

week = 1
url = 'http://www.nfl.com/liveupdate/scores/scores.json'

game = models.Schedule.query.filter_by(week=week,home_team=homeTeam).first()

r = requests.get(url)
jsonScores =  r.json()


for gameScore in jsonScores:
    if jsonScores[gameScore]['qtr'] == 'Final':
        print "--------------------------------"
        print gameScore
        print jsonScores[gameScore]['home']['abbr']
        print jsonScores[gameScore]['home']['score']['T']
        print jsonScores[gameScore]['away']['abbr']
        print jsonScores[gameScore]['away']['score']['T']
