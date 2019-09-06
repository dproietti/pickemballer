import urllib2
import xml.dom.minidom as xml
import time

# comment

def schedule_url(year, stype, week):
    """
    Returns the NFL.com XML schedule URL. `year` should be an
    integer, `stype` should be one of the strings `PRE`, `REG` or
    `POST`, and `gsis_week` should be a value in the range
    `[0, 17]`.
    """
    xmlurl = 'http://www.nfl.com/ajax/scorestrip?'
    if stype == 'POST':
        week += 17
        if week == 21:  # NFL.com you so silly
            week += 1
    return '%sseason=%d&seasonType=%s&week=%d' % (xmlurl, year, stype, week)


def week_schedule(year, stype, week):
    """
    Returns a list of dictionaries with information about each game in
    the week specified. The games are ordered by gsis_id. `year` should
    be an integer, `stype` should be one of the strings `PRE`, `REG` or
    `POST`, and `gsis_week` should be a value in the range `[1, 17]`.
    """
    url = schedule_url(year, stype, week)
    try:
        dom = xml.parse(urllib2.urlopen(url))
    except urllib2.HTTPError:
        print >> sys.stderr, 'Could not load %s' % url
        return []

    games = []
    for g in dom.getElementsByTagName("g"):
        gsis_id = g.getAttribute('eid')
        games.append({
            'eid': gsis_id,
            'wday': g.getAttribute('d'),
            'year': year,
            'month': int(gsis_id[4:6]),
            'day': int(gsis_id[6:8]),
            'time': g.getAttribute('t'),
            'meridiem': None,
            'season_type': stype,
            'week': week,
            'home': g.getAttribute('h'),
            'away': g.getAttribute('v'),
            'gamekey': g.getAttribute('gsis'),
        })

    for game in games:
        h = int(game['time'].split(':')[0])
        m = int(game['time'].split(':')[1])
        if 0 < h <= 5:  # All games before "6:00" are PM until proven otherwise
            game['meridiem'] = 'PM'

        if game['meridiem'] is None:

            days_games = [g for g in games if g['wday'] == game['wday']]
            preceeding = [g for g in days_games if g['eid'] < game['eid']]
            proceeding = [g for g in days_games if g['eid'] > game['eid']]

            # If any games *after* this one are AM then so is this
            if any(g['meridiem'] == 'AM' for g in proceeding):
                game['meridiem'] = 'AM'
            # If any games *before* this one are PM then so is this one
            elif any(g['meridiem'] == 'PM' for g in preceeding):
                game['meridiem'] = 'PM'
            # If any games *after* this one have an "earlier" start it's AM
            elif any(h > t for t in [int(g['time'].split(':')[0]) for g in proceeding]):
                game['meridiem'] = 'AM'
            # If any games *before* this one have a "later" start time it's PM
            elif any(h < t for t in [int(g['time'].split(':')[0]) for g in preceeding]):
                game['meridiem'] = 'PM'

        if game['meridiem'] is None:
            if game['wday'] not in ['Sat', 'Sun']:
                game['meridiem'] = 'PM'
            if game['season_type'] == 'POST':
                game['meridiem'] = 'PM'

    return games

for week in range(1,18):
    #print "week: %s" % week
    games = week_schedule(year=2019, stype='REG', week=week)
    weekGameId = 0
    for game in games:
        #print game
        startTimeString = ("%s-%s-%s %s %s" % ( game['year'], game['month'], game['day'], game['time'], game['meridiem']))
        #print startTimeString
        startTime = time.strptime(startTimeString, "%Y-%m-%d %I:%M %p")
        #print time.strftime('%Y-%m-%d %H:%M:%S', startTime)
        weekGameId += 1
        sql = "INSERT INTO schedule (id, eid, week, start_time ,home_team, away_team, week_game_id) VALUES (%s, %s, %s, '%s', '%s', '%s', %s);"
        print sql % (game['gamekey'], game['eid'], game['week'], time.strftime('%Y-%m-%d %H:%M:%S', startTime), game['home'],game['away'], weekGameId)


#// time.strptime("2017-12-31 1:00 PM", "%Y-%m-%d %I:%M %p")
#// startTime = time.strptime("2017-12-31 1:00 PM", "%Y-%m-%d %I:%M %p")
#

