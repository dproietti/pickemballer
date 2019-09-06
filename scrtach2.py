
from app import db, models

for game in models.Schedule.query.filter(models.Schedule.week==4):
    print game
    print game.home_score
    print game.away_score
    print "Winner: %s" % game.atsWinner()