
import sys
import csv
import datetime
from app import db, models

def getCurrentNFLWeek():
    dt = datetime.datetime.now()
    if dt.isocalendar()[2] in [4,5,6,7]:
        return dt.isocalendar()[1] - 35
    else:
        return dt.isocalendar()[1] - 36

def addPointSpread(week, homeTeam, homeLine, awayLine, overUnder):
    game = models.Schedule.query.filter_by(week=week,home_team=homeTeam).first()                                                                          
    game.home_line = homeLine
    game.away_line = awayLine
    game.over_under = overUnder
    db.session.commit()

year = 2016
week = -1

if len(sys.argv) >=2:
    week = sys.argv[1]
else:
    week = getCurrentNFLWeek()
    
teams = {}

for team in models.Team.query.all():
    teams[team.name.upper()] = team.id

##['1 JETS', '5:25 PM', '2 BILLS*', '1']

#print teams
with open('data/week-2-spread.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        print row
        homeTeam = None
        homeSpread = None
        if '*' in row[0]:
            homeTeam = row[0].split(' ')[1]
            homeSpread = float(row[3]) * -1    
        else:
            homeTeam = row[2].split(' ')[1]
            homeSpread = float(row[3]) 
        
        homeTeam = homeTeam.replace('*', '')
        print "home team: %s (%s)" % (homeTeam , homeSpread)
            
        addPointSpread(week=week,
            homeTeam = teams[homeTeam],
            homeLine = homeSpread, 
            awayLine = homeSpread * -1 , 
            overUnder = None )

        
        

#with requests.Session() as s:
#    download = s.get(url)
#    decoded_content = download.content.decode('utf-8')
#    input_file = csv.DictReader(decoded_content.splitlines(), delimiter=',')
    
#    for row in input_file:
#        if row['home_team'] == 'JAC':
#            row['home_team'] = 'JAX'

        #print "home team: %s" % row['home_team']
        #print "home line: %s" % row['home_line']
        

