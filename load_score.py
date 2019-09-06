
from app import db, models
import sys

import datetime

#Ussage <week> <home team> <home score> <away score>

week = sys.argv[1]
homeTeam = sys.argv[2]
homeScore = int(sys.argv[3])
awayScore = int(sys.argv[4])

print "week: %s, home team: %s, home score %s, away score %s" % (week, homeTeam, homeScore, awayScore)


game = models.Schedule.query.filter_by(week=week,home_team=homeTeam).first()

game.home_score = homeScore
game.away_score = awayScore

#update team win/loss/tie summary'
homeTeam = models.Team.query.get(game.home_team)
awayTeam = models.Team.query.get(game.away_team)

if homeScore > awayScore:
    homeTeam.wins += 1
    awayTeam.losses += 1
elif homeScore < awayScore:
    homeTeam.losses += 1
    awayTeam.wins += 1
else:
    homeTeam.ties += 1
    awayTeam.ties += 1

winner = game.atsWinner()

for pic in models.Pics.query.filter_by(week=week):
    if getattr(pic, 'game_' + str(game.week_game_id)) == winner:
        pic.wins += 1

db.session.commit()

print "Added Score for Week: %s Game(eid): %s %s(%s) @ %s(%s)" % (week, game.eid, awayTeam.id, awayScore, homeTeam.id, homeScore)

