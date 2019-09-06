
from app import db, models
from sqlalchemy.sql import func
import sys

week = sys.argv[1]
print "week: %s" % week

from sqlalchemy.sql.expression import func

## what is tieBreaker Game for the week
qry =  db.session.query(func.max(models.Schedule.week_game_id).label("tieBreakerGameId")).filter_by(week=week)
res = qry.one()
tieBreakerGameId = res.tieBreakerGameId
print "Tie Breaker Game ID: %s" % tieBreakerGameId

schedule = models.Schedule.query.filter_by(week=week, week_game_id=tieBreakerGameId).first()
tieBreakerGameTotalScore = schedule.home_score + schedule.away_score
print "Tie Breaker Score: %s" % tieBreakerGameTotalScore



qry =  db.session.query(func.max(models.Pics.wins).label("max_wins")).filter_by(week=week,pool_id=2)
res = qry.one()
wins = res.max_wins
print "Max wins: %s" % wins

pics = models.Pics.query.filter_by(week=week, wins=wins, pool_id=2).all() 

if len(pics) == 1:
    for pic in pics:
        pic.winner = True
        pic.winnerTieBreaker = None
        db.session.commit()
else:
    print "Number of Winners: %s" % len(pics)
    print pics
    
    lowestDiff = 1000
    winners = []
    
    tieBrakerPics = {}
    for pic in pics:
        print pic
        print pic.tieBreaker
        
        if pic.tieBreaker == tieBreakerGameTotalScore:
            tieBrakerPics[pic.id] = 0
        elif pic.tieBreaker < tieBreakerGameTotalScore:
            tieBrakerPics[pic.id] = tieBreakerGameTotalScore - pic.tieBreaker
        else:
            tieBrakerPics[pic.id] = pic.tieBreaker - tieBreakerGameTotalScore
        print "Tie Breaker, Id: %s, Diff %s" % (pic.id, tieBrakerPics[pic.id])
        tieBreakerDiff = tieBrakerPics[pic.id]
        if tieBreakerDiff == lowestDiff:
            winners.append(pic.id)
        elif tieBreakerDiff < lowestDiff:
            winners = []
            lowestDiff = tieBreakerDiff
            winners.append(pic.id)
    
    print winners
    for winner in winners:
        pics = models.Pics.query.get(winner)
        pics.winner = True
        pics.winnerTieBreaker = True
        db.session.commit()
        