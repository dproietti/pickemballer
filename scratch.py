
from app import db, models

week=0
week_game_num = 0
for game in models.Schedule.query.all():
    if week <> game.week:
        week = game.week
        week_game_num = 1
    else:
        week_game_num +=1
    
    game.week_game_id = week_game_num
    print "gid %s, week %s, game # %s" % (game.id,  week, week_game_num)

db.session.commit()