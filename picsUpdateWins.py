
from app import db, models, utils
import sys

week = sys.argv[1]
print "week: %s" % week

games = models.Schedule.query.filter(models.Schedule.week==week)

## Update Wins
for pic in models.Pics.query.filter(models.Pics.week==week):
    wins = 0
    gameCounter = 0
    for game in games:
        gameCounter +=1
        if getattr(pic, 'game_' + str(gameCounter)) == game.atsWinner():
            wins += 1
        
    pic.wins = wins
    print "Player: %s wins: %s" % (models.Player.query.get(pic.player_id).name(), pic.wins)
    db.session.commit()
    