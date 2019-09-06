
from app import db, models
from sqlalchemy import func

for game in models.Schedule.query.filter(models.Schedule.week==4):
    print game
    print game.home_score
    print game.away_score
    print "Winner: %s" % game.atsWinner()
    
#for pic in models.Pics.query(models.Pics.player_id, func.sum(models.Pics.wins)).group_by(models.Pics.player_id).all():
for pic in models.Pics.query.filter(models.Pics.pool_id ==2):
    print pic.player_id


for pic in db.session.query(models.Pics).all():
    print pic.player_id

#for pic in db.session.query(models.Pics).group_by(models.Pics.player_id, func.sum(models.Pics.wins)).filter(models.Pics.pool_id ==2):
#    print pic

sql = """
SELECT player.id, player.firstname, player.lastname, sum(pics.wins) as winsTotal 
FROM pics 
INNER JOIN player ON player.id = pics.player_id
WHERE pics.pool_id = 2 
GROUP BY player.id, player.firstname, player.lastname
ORDER BY winsTotal desc;"""

result = db.engine.execute(sql)
for row in result:
    print 
    
    
def getSeasonStandings():
    sql = """
    SELECT player.id, player.firstname, player.lastname, sum(pics.wins) as winsTotal 
    FROM pics 
    INNER JOIN player ON player.id = pics.player_id
    WHERE pics.pool_id = 2 
    GROUP BY player.id, player.firstname, player.lastname
    ORDER BY winsTotal desc;"""

    result = db.engine.execute(sql)
    results = []
    for row in result:
        results.append({ 'player' : "%s %s " % (row.firstname, row.lastname), 'wins': row.winsTotal})
       
    return results

print getSeasonStandings()