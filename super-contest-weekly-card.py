
import sys
import datetime
from bs4 import BeautifulSoup
import requests
from app import db, models
import re

def getCurrentNFLWeek():
    dt = datetime.datetime.now()
    if dt.isocalendar()[2] in [4,5,6,7]:
        return dt.isocalendar()[1] - 35
    else:
        return dt.isocalendar()[1] - 36
        
def isGame(week, homeTeam, awayTeam):
    game = models.Schedule.query.filter_by(week=week,home_team=homeTeam, away_team=awayTeam).first() 
    if game:
    	return True
    else:
    	return False
    

def addPointSpread(week, homeTeam, homeLine, awayTeam, awayLine, overUnder):
    game = models.Schedule.query.filter_by(week=week,home_team=homeTeam, away_team=awayTeam).first() 
    if game:
    	game.home_line = homeLine
    	game.away_line = awayLine
    	game.over_under = overUnder
    	db.session.commit()
    else:
    	raise ValueError('No game in week %s matches Home Team: %s vs Away Team: %s' % (week, homeTeam, awayTeam))


def cleanupTeamName(team):
	if '49ERS' in team:
		return '49ERS'
	else:
		teamName = team.replace('*', '')
		teamName = re.sub(r'\d+', '', teamName)
		return teamName.strip()
	
year = 2016
week = -1
if len(sys.argv) >=2:
    week = sys.argv[1]
else:
    week = getCurrentNFLWeek()

print "Week: %s" % week
    
teams = {}

for team in models.Team.query.all():
    teams[team.name.upper()] = team.id
    
url = "https://www.westgatedestinations.com/nevada/las-vegas/westgate-las-vegas-hotel-casino/casino/supercontest-weekly-card"
print "URL: %s" % url
r  = requests.get(url)
data = r.text

soup = BeautifulSoup(data,"html5lib")
rows =soup.find('table', class_='table table-striped table-bordered').find_all("tr")
for row in rows:
	cells = row.find_all("td")
	teamCol1 = cells[0].get_text()
	teamCol2 = cells[2].get_text()
	spreadCell = cells[3].get_text()
	#print "team1: %s, team2: %s, spread: %s" % (teamCol1, teamCol2, spreadCell)
	
	if teamCol1 and teamCol2 and spreadCell:
		awayTeam = None
		homeTeam = None
		homeSpread = None
		awaySpread = None
		spread = None
		
		if spreadCell == 'PK':
			spread = 0
		elif spreadCell== 'PPD':
			spread = 0
		else:
			spread = float(spreadCell)
		
		if '*' in teamCol1:
			homeTeam = cleanupTeamName(teamCol1)
			awayTeam = cleanupTeamName(teamCol2)
			homeSpread = spread * -1
			awaySpread = spread
		elif '*' in teamCol2:
			homeTeam = cleanupTeamName(teamCol2)
			awayTeam = cleanupTeamName(teamCol1)
			homeSpread = spread 
			awaySpread = spread * -1
		else:  ## foreign games with no home team marked
			if isGame(week=week, homeTeam=teams[teamCol1.split(' ')[1]], awayTeam=teams[teamCol2.split(' ')[1]]):
				homeTeam = cleanupTeamName(teamCol1)
				awayTeam = cleanupTeamName(teamCol2)
				homeSpread = spread * -1
				awaySpread = spread
			else:
				homeTeam = cleanupTeamName(teamCol2)
				awayTeam = cleanupTeamName(teamCol1)
				homeSpread = spread
				awaySpread = spread * -1
				
				
			
		#homeTeam = homeTeam.replace('*', '')
		#awaySpread = homeSpread * -1
		
		print "Game: %s-%s (%s) @ %s-%s (%s)" % ( awayTeam, teams[awayTeam], awaySpread,homeTeam, teams[homeTeam], homeSpread )
		addPointSpread(week=week, homeTeam=teams[homeTeam], homeLine=homeSpread, awayTeam=teams[awayTeam], awayLine=awaySpread, overUnder=None )
			
			
			
