
import requests

class Score(object):
    def __init__(self, game):
        self.teamHome = game['home']['abbr']
        self.teamAway = game['away']['abbr']
        
    
    

url = 'http://www.nfl.com/liveupdate/scores/scores.json'
r = requests.get(url)
jsonScores =  r.json()

#print jsonScores

for gameId in jsonScores:
    game = jsonScores[gameId]
    score = Score(game)
    #print game
    #if not(game['qtr'] == 'Final' or game['qtr'] == 'final overtime' or game['qtr'] == None):
    if not(game['qtr'] == 'Final' or game['qtr'] == 'final overtime'):
        
        print ""
        print "Away: %s %s" % ( game['away']['abbr'], game['away']['score']['T'] )
        print "Home: %s %s" % ( game['home']['abbr'], game['home']['score']['T'] )
        print "qtr: %s" % game['qtr']
        if not(game['qtr'] == 'Final' or game['qtr'] == 'final overtime' or game['qtr'] == 'Halftime'):
            ##print "Game On"
            print "clock: %s" % game['clock']
            print "Possession: %s" % game['posteam']
            print "Down: %s" % game['down']
            print "ToGo %s" % game['togo']
            print "Yardline: %s" % game['yl']
            print "Big Plays: %s" % game['bp']
            if game['note']:
                print "Note: %s" % game['note']
        
        