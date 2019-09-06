
import sys
from app import db, models

def addPointSpread(week, homeTeam, homeLine, awayLine, overUnder):
    game = models.Schedule.query.filter_by(week=week,home_team=homeTeam).first()                                                                          
    game.home_line = homeLine
    game.away_line = awayLine
    game.over_under = overUnder
    db.session.commit()


overUnder = None

week = sys.argv[1]
homeTeam = sys.argv[2]
homeLine = float(sys.argv[3])
awayLine = homeLine * -1
if len(sys.argv) >= 5:
    overUnder = sys.argv[4]

print "Add Spread: Week: %s, Home Team: %s, Home Line: %s, Over/Under: %s" % (week, homeTeam, homeLine, overUnder)
addPointSpread(week=week, homeTeam=homeTeam, homeLine=homeLine, awayLine=awayLine, overUnder=overUnder)

print "CmdLine %s" % str(sys.argv)
print "Add Spread: Week: %s, Home Team: %s, Home Line: %s, Over/Under: %s" % (week, homeTeam, homeLine, overUnder)
