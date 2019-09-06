
from app import db, models, utils
import requests
import datetime


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
print "Current Date Time: %s" % dt.strftime("%Y-%m-%d %X" )
if models.Schedule.query.filter(models.Schedule.week==week, models.Schedule.home_score==None, models.Schedule.start_time < dt).first():
    for game in models.Schedule.query.filter(models.Schedule.week==week, models.Schedule.home_score==None, models.Schedule.start_time < dt):
        print game
        eid = str(game.eid)
        if jsonScores[eid]['qtr'] == 'Final' or jsonScores[eid]['qtr'] == 'final overtime':
            
            #print "Raw Data: %s: " % jsonScores[eid]
            homeScore = int(jsonScores[eid]['home']['score']['T'])
            awayScore = int(jsonScores[eid]['away']['score']['T'])
            
            #update score on schedule
            game.home_score = homeScore
            game.away_score = awayScore
            
            #adjust for JAC/JAX abnormality
            if jsonScores[eid]['home']['abbr'] == 'JAC':
                jsonScores[eid]['home']['abbr'] = 'JAX'
            
            if jsonScores[eid]['away']['abbr'] == 'JAC':
                jsonScores[eid]['away']['abbr'] = 'JAX'
            
            #update team win/loss/tie summary'    
            homeTeam = models.Team.query.get(jsonScores[eid]['home']['abbr'])
            awayTeam = models.Team.query.get(jsonScores[eid]['away']['abbr'])
            
            if homeScore > awayScore:
                homeTeam.wins += 1
                awayTeam.losses += 1
            elif homeScore < awayScore:
                homeTeam.losses += 1
                awayTeam.wins += 1
            else:
                homeTeam.ties += 1
                awayTeam.ties += 1
            
            db.session.commit()
            
            print "Added Score for Week: %s Game(eid): %s %s(%s) @ %s(%s)" % (week, game.eid, awayTeam.id, awayScore, homeTeam.id, homeScore)
        else:
            "Game: %s@%s not finised" % (models.Team.query.get(jsonScores[eid]['away']['abbr']), models.Team.query.get(jsonScores[eid]['home']['abbr']))
            
else:
    print "No games to update"
    
    
## Update Wins
games = models.Schedule.query.filter(models.Schedule.week==week).order_by(models.Schedule.week_game_id)

for pic in models.Pics.query.filter(models.Pics.week==week):
    wins = 0
    for game in games:
        playerGamePic = getattr(pic, 'game_' + str(game.week_game_id))
        if playerGamePic is not None and playerGamePic == game.atsWinner():
            wins += 1
            #print "Win: %s Game(eid): %s %s(%s) @ %s(%s)" % (week, game.eid, game.away_team, game.away_score, game.home_team, game.home_score)
        
    pic.wins = wins
    print "Player: %s wins: %s" % (models.Player.query.get(pic.player_id).name(), pic.wins)
    db.session.commit()
