
from app import db, models, utils
import requests
import datetime

week = utils.getCurrentNFLWeek()
url = 'http://www.nfl.com/liveupdate/scores/scores.json'
print "Week: %s" % week
print "URL: %s" % url
for game in models.Schedule.query.filter(models.Schedule.week==week):
    winner = None
    if game.atsWinner():
        winner = game.home_team
    elif game.atsWinner() == False:
        winner = game.away_team
    else:
        winner = ""
    print "%s @ %s ats winner: %s" % (game.away_team, game.home_team, winner)
    
