
from app import db, models, utils
import requests
import datetime

week = utils.getCurrentNFLWeek()
url = 'http://www.nfl.com/liveupdate/scores/scores.json'
print "Week: %s" % week
print "URL: %s" % url

## build distribution list
email_to = ""

for poolPlayer in models.PoolPlayer.query.filter(models.PoolPlayer.pool_id==2):
    email_to += models.Player.query.get(poolPlayer.player_id).email + " ; "

print "Email To: %s" % email_to
print "Subject: Week %s spreads - Make your picks" % week

for game in models.Schedule.query.filter(models.Schedule.week==week):
    print "%s (%s) @ %s (%s)" % (game.away_team, game.away_line, game.home_team, game.home_line)
