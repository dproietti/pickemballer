
from app import app, db, utils, models, emails

import os
from jinja2 import Environment, FileSystemLoader
 
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'app', 'templates')),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


week = utils.getCurrentNFLWeek()
teams = utils.getTeams()


subject = "Make your pics for week %s, week Locks at %s" % (week, utils.startTimeOfFirstGame(week=week).strftime("%A,s %I:%M %p"))
games = []
for game in models.Schedule.query.filter_by(week=week):
    games.append({
        'home_team' : teams[game.home_team],
        'away_team' : teams[game.away_team],
        'away_line' : game.away_line,
        'home_line' : game.home_line,
        'over_under' : game.over_under
        }
    )
   
overUnderGame = games[len(games) -1]

#print subject
#print games
#print overUnderGame

print ""
print ""
print ""
print ""
print "PATH: %s" % os.path.join(PATH, 'app', 'templates')
#print TEMPLATE_ENVIRONMENT

context = {
    'week' : week,
    'games': games,
    'overUnderGame' : overUnderGame
}

print context
print render_template('email-sow.txt', context)
print render_template('email-sow.html', context)

#emails.send_email_templates(subject=subject, games=games, overUnderGame=overUnderGame)

emails.send_email(subject = subject,
            sender = 'noreply@pickemballer.com',
            recipients = 'daniel.proietti@gmail.com',
            text_body=render_template('email-sow.txt', context) ,
            html_body=render_template('email-sow.html', context))

