import uuid
import datetime
from pytz import timezone

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, \
    login_required
from app import app, db, lm, bcrypt, Mail
from .forms import LoginForm, RegistrationForm, PoolForm, ActivateUserForm, picsForm, PasswordReset, PoolAddPlayer, PasswordChange, AddSpread
from .models import Player, Pool, PoolPlayer, Team, Schedule, Pics
from .emails import send_email

    
def getUserName():
    if current_user.is_authenticated:
        player = current_user
        return player.email
    else:
        return None

def getCurrentWeek():
    if 'current_week' in session:
        return session['current_week']
    else:
        dt = datetime.datetime.now()
        cWeek = 1
        if dt.isocalendar()[2] in [4,5,6,7]:
            cWeek = dt.isocalendar()[1] - 35
        else:
            cWeek = dt.isocalendar()[1] - 36
        if cWeek < 1:
            return 1
        elif cWeek > 17:
            return 17
        else:
            return cWeek
            

def getCurrentPool():
    if 'current_pool' in session:
        return session['current_pool']
    else:
        for pools in getPools():
            session['current_pool'] = pools['id']
            return session['current_pool']
    
    return None

def getTeams():
    teams = {}
    for team in Team.query.all():
        teams[team.id] = team
    return teams

def getGamesPerWeek(week):
    # 2016 weeks = [0, 16, 16, 16, 15, 14, 15, 15, 13, 13, 14, 14, 16, 15, 16, 16, 16, 16]
    # 2017 weeks = [0, 16, 16, 16, 16, 14, 14, 15, 13, 13, 14, 13, 16, 16, 16, 16, 16, 16]
    # 2018 weeks = [0, 16, 16, 16, 15, 15, 15, 14, 14, 13, 14, 13, 15, 16, 16, 16, 16, 16]
    weeks = [0, 16, 16, 16, 15, 15, 14, 14, 15, 14, 13, 14, 14, 16, 16, 16, 16, 16]
    return weeks[week]

@lm.user_loader
def user_loader(id):
    return Player.query.get(id)

def getPools():
    pools = []
    for poolPlayer, pool in db.session.query(PoolPlayer, Pool).join(Pool).filter(PoolPlayer.player_id==current_user.id).all():
        pools.append({'name' : pool.name , 'id' : str(pool.id)})
    return pools

def getCommissionerPools():
    pools = []
    for pool in Pool.query.filter_by(commissioner=current_user.id):
        pools.append({'name' : pool.name , 'id' : str(pool.id), 'type': pool.type})
    return pools

def getCurrentAdminPool():
    
    if 'current_admin_pool_id' in session:
        pool = Pool.query.get(session['current_admin_pool_id'])
        return {'name' : pool.name , 'id' : str(pool.id), 'type': pool.type}
    else:
        pools = getCommissionerPools()
        if pools:
            pool = pools[0]
            session['current_admin_pool_id'] = pool['id']
            return pool
    
    return None

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
    
###############################################################################
# Index
###############################################################################
@app.route('/')
@app.route('/index')
def index():
    if getUserName() == None:
         return redirect(url_for('login'))

    if request.method == 'GET':
        if 'week' in request.args:
            session['current_week'] = int(request.args.get('week'))

    if request.method == 'GET':
        if 'pool' in request.args:
            session['current_pool'] = request.args.get('pool')
            
    dspPics = []
    weekGames = []
    for game in Schedule.query.filter(Schedule.week==getCurrentWeek()).order_by(Schedule.week_game_id):
        weekGames.append([game.home_team, game.away_team, game.atsWinner(), game.gameStarted()])
        
    for player, pic in db.session.query(Player, Pics).join(Pics).filter_by(pool_id=getCurrentPool(), week=getCurrentWeek()).order_by(Pics.wins.desc(),Pics.winner.desc()).all():
        games = []
        gameCounter = 0
        showPicks = pic.showPicks or player.id == current_user.id

        for game in weekGames:
            gameCounter += 1
            isWinner = False
            if getattr(pic, 'game_' + str(gameCounter)) == game[2]:
                isWinner = True
                
            if pic.showPicks or player.id == current_user.id or game[3]:
                if  getattr(pic, 'game_' + str(gameCounter)) == 1:
                    games.append({'team' : game[0], 'win' : isWinner })
                elif getattr(pic, 'game_' + str(gameCounter)) == 0:
                    games.append({'team' : game[1], 'win' : isWinner })
                else:
                    games.append({'team' : '---', 'win' : False })
            else:
                games.append({'team' : '***', 'win' : False })
        
        game = weekGames[len(weekGames)-1]
        if pic.showPicks or player.id == current_user.id or game[3]: 
            tieBreaker = pic.tieBreaker
        else:
            tieBreaker = "***"
        
        dspPics.append({'player' : player.name(), 'games' : games, 'over_under' : tieBreaker, 'over_under_winner' : pic.winnerTieBreaker, 'wins' : pic.wins, 'winner' : pic.winner})

    return render_template("index.html",
                       username=getUserName(),
                       pools = getPools(),
                       pics=dspPics,
                       current_week = getCurrentWeek(),
                       current_pool = getCurrentPool(),
                       poolAdmin = current_user.poolAdmin,
                       number_of_games = getGamesPerWeek(getCurrentWeek()),
                       seasonStandings = getSeasonStandings())

###############################################################################
# Pics
###############################################################################
@app.route('/pics', methods=['GET', 'POST'])
def pics():
    if getUserName() == None:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        if 'week' in request.args:
            session['current_week'] = int(request.args.get('week'))

    if request.method == 'GET':
        if 'pool' in request.args:
            session['current_pool'] = request.args.get('pool')
    
    pics = None
    if request.method == 'GET':
        pics = Pics.query.filter_by(pool_id=getCurrentPool(), player_id=current_user.id, week=getCurrentWeek()).first()
        if pics is None:
            pics = None
    elif request.method == 'POST':
        pics = Pics.query.filter_by(pool_id=getCurrentPool(), player_id=current_user.id, week=getCurrentWeek()).first()
        if pics is None:
            pics = Pics(pool_id=getCurrentPool(), player_id=current_user.id, week=getCurrentWeek())

    gameCounter = 0
    pickCounter = 0
    overUnder =  None
    overUnderTeamAway = None
    overUnderTeamHome = None
    tieBreakerLocked = False
    
    display_pics = []
    teams = getTeams()
    for game in Schedule.query.filter(Schedule.week==getCurrentWeek()).order_by(Schedule.week_game_id):
        display_pic = {}
        display_pic['game_id'] = game.week_game_id
        display_pic['away_team'] = teams[game.away_team]
        display_pic['away_line'] = game.away_line
        display_pic['home_team'] = teams[game.home_team]
        display_pic['home_line'] = game.home_line
        display_pic['home_pick'] = None
        display_pic['away_pick'] = None
        display_pic['locked'] = game.gameStarted()
        tieBreakerLocked = game.gameStarted()
        overUnder = game.over_under
        overUnderTeamAway = teams[game.away_team].name
        overUnderTeamHome = teams[game.home_team].name
        display_pic['tie_breaker'] = None
        if request.method == 'POST':
            if str(game.week_game_id) in request.form:
                gamePick = None
                if request.form[str(game.week_game_id)] == 'H':
                    display_pic['home_pick'] = True
                    gamePick = True
                    pickCounter += 1
                elif request.form[str(game.week_game_id)] == 'A':
                    display_pic['away_pick'] = True
                    gamePick = False
                    pickCounter += 1
                if not game.gameStarted():
                    setattr(pics, 'game_' + str(game.week_game_id), gamePick )
                else:
                    print "Game Locked: %s" % game.week_game_id
            if  getattr(pics, 'game_' + str(game.week_game_id)) == 1:
                display_pic['home_pick'] =  True
                pickCounter += 1
            elif getattr(pics, 'game_' + str(game.week_game_id)) == 0:
                display_pic['away_pick'] =  True
                pickCounter += 1
        elif request.method == 'GET':
            if pics is not None:
                if  getattr(pics, 'game_' + str(game.week_game_id)) == 1:
                    display_pic['home_pick'] =  True
                elif getattr(pics, 'game_' + str(game.week_game_id)) == 0:
                    display_pic['away_pick'] =  True

        display_pics.append(display_pic)

    if request.method == 'POST':
        if pics.id <= 0:
            db.session.add(pics)
        pics.tieBreaker = request.form['tieBreaker']
        if 'showPicks' in request.form:
            pics.showPicks = True
        else:
            pics.showPicks = False
        db.session.commit()
        flash("pics saved", 'info')
        if pickCounter < game.week_game_id:
            flash("Your missing %s picks" % (game.week_game_id - pickCounter), "warning")
        if pics.tieBreaker == 0:
            flash("Your missing the tie breaker", "warning")
    
    if pics is not None:
        tieBreaker = pics.tieBreaker
        showPicks = pics.showPicks
    else:
        tieBreaker = 0
        showPicks = False
    
    form = picsForm()
    form.tieBreaker.data = tieBreaker
    form.showPicks.data = showPicks
    
    return render_template("pics.html", 
                            username=getUserName(), 
                            pics=display_pics, 
                            pools = getPools(),
                            current_week = getCurrentWeek(),
                            current_pool = getCurrentPool(),
                            tieBreaker=tieBreaker,
                            tieBreakerLocked=tieBreakerLocked,
                            showPicks=showPicks,
                            overUnder = overUnder,
                            overUnderTeamAway = overUnderTeamAway,
                            overUnderTeamHome = overUnderTeamHome,
                            poolAdmin = current_user.poolAdmin,
                            form=form)

###############################################################################
# login
###############################################################################
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        player = Player.query.filter_by(email=form.email.data.lower()).first()
        if player != None:
            if bcrypt.check_password_hash(player.password, form.password.data):
                login_user(player)
                flash('You were successfully logged in', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid Login', 'danger')
                return render_template("login.html", loginForm=LoginForm())
        else:
            flash('Invalid Login', 'danger')
            return render_template("login.html", loginForm=LoginForm())
    else:
        return render_template("login.html", loginForm=LoginForm())

###############################################################################
# logout
###############################################################################    
@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))
    
###############################################################################
# register user
###############################################################################    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST':

        if form.validate():

            if db.session.query(db.exists().where(Player.email == form.email.data.lower())).scalar():
                return redirect(url_for('do_error', messages="User with email exists!"))
            else:
                player = Player(
                    firstname = form.firstname.data,
                    lastname = form.lastname.data,
                    email = form.email.data.lower(),
                    password = bcrypt.generate_password_hash(form.password.data))
                db.session.add(player)
                db.session.commit()
                flash('Thanks for registering')
                login_user(player)
                return redirect(url_for('index'))

    return render_template('register.html', form=form)
  
###############################################################################
# activate user
###############################################################################    
@app.route('/activate/<setpwdkey>', methods=['GET', 'POST'])
def activate(setpwdkey):
    form = ActivateUserForm(request.form)
    
    if request.method == 'GET':
    
        player = Player.query.filter_by(setpwdkey=setpwdkey).first()
        if player:
            return render_template('activate.html', form=form, setpwdkey=setpwdkey, email=player.email)
        else:
            return redirect(url_for('do_error', messages="player does not exists"))
    elif request.method == 'POST':
        player = Player.query.filter_by(setpwdkey=setpwdkey).first()
        if form.validate():
            player.firstname = form.firstname.data
            player.lastname = form.lastname.data
            player.password = bcrypt.generate_password_hash(form.password.data)
            player.setpwdkey = None
            db.session.add(player)
            db.session.commit()
            flash('Thanks for activating')
            login_user(player)
            return redirect(url_for('index'))        
        else:
            return render_template('activate.html', form=form, setpwdkey=setpwdkey, email=player.email)
            
###############################################################################
# Change Password
###############################################################################
@app.route('/password-change', methods=['GET', 'POST'])
def passwordChnage():
    if getUserName() == None:
        return redirect(url_for('login'))

    form = PasswordChange(request.form)
    if request.method == 'GET':
        return render_template('password-change.html', 
                            username=getUserName(), 
                            poolAdmin = current_user.poolAdmin,
                            form=form)
    elif request.method == 'POST':
        if form.validate():
            player = current_user
            if player.validatePassword(form.passwordOld.data):
                flash("password changed!", 'info')
                player.setPassword(form.passwordNew.data)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('Invalid Old Password', 'danger')
                return render_template('password-change.html', 
                            username=getUserName(), 
                            poolAdmin = current_user.poolAdmin,
                            form=form)                
        else:
            for errors in form.errors.items():
                for error in errors:
                    flash(u"%s" % ( error), 'danger')
                    
            #flash("invalid!", 'info')
            return render_template('password-change.html', 
                            username=getUserName(), 
                            poolAdmin = current_user.poolAdmin,
                            form=form)
                            
###############################################################################
# Reset Password
###############################################################################
@app.route('/password-reset', methods=['GET', 'POST'])
def passwordReset():
    form = PasswordReset(request.form)
    if request.method == 'GET':
        return render_template('password-reset.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            player = Player.query.filter_by(email=form.email.data.lower()).first()
            if player:
                newPassword = str(uuid.uuid4().get_hex().upper()[0:6])
                player.password = bcrypt.generate_password_hash(newPassword)
                db.session.commit()
    
                send_email(subject = 'password reset',
                            sender = 'noreply@pickemballer.com',
                            recipients = player.email,
                            text_body='password has been reset to = %s' % newPassword ,
                            html_body=None)
                
                flash("password reset, check your email!", 'info')
                return redirect(url_for('login'))  
            else:
                flash("unknown email %s" % form.email.data, 'danger')
                return render_template('password-reset.html', form=form)
        else:
            for errors in form.errors.items():
                for error in errors:
                    flash(u"%s" % ( error), 'danger')
            return render_template('password-reset.html', form=form)

###############################################################################
# pool 
###############################################################################    
@app.route('/pool', methods=['GET', 'POST'])
def pool():
    if getUserName() == None:
         return redirect(url_for('login'))

    poolForm = PoolForm(request.form)
    if request.method == 'POST':
        if poolForm.validate():
            player = current_user
            pool = Pool(name=poolForm.poolname.data, commissioner=player.id, type=poolForm.pooltype.data)
            db.session.add(pool)
            db.session.flush()
            poolPlayer = PoolPlayer(pool=pool, player=player, nickName=player.name(), commissioner=True, accepted=True)
            db.session.add(poolPlayer)
            db.session.commit()
            
            return redirect(url_for('index'))
    elif 'pool_name' in session:
        poolForm.poolname.data = session['pool_name']
        poolForm.pooltype.data = session['pool_type']

    return render_template('pool.html', username=getUserName(), form=poolForm)

###############################################################################
# admin -add spreads 
###############################################################################    
@app.route('/admin-addspreads',  methods=['GET', 'POST'])
def adminAddSpread():

    if getUserName() == None:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        if 'pool' in request.args:
            session['current_admin_pool_id'] = request.args.get('pool')
    
    if request.method == 'GET':
        if 'week' in request.args:
            session['current_week'] = int(request.args.get('week'))
            
    if request.method == 'POST':
        addSpreadForm = AddSpread(request.form)
        game = Schedule.query.get(addSpreadForm.gameId.data)
        if game.gameStarted():
            flash("spread not save because game started ( %s @ %s )" % ( game.away_team, game.home_team )  , 'warning')
        else:
            game.home_line = addSpreadForm.homeLine.data
            game.away_line = game.home_line * -1
            game.over_under = addSpreadForm.overUnder.data
            db.session.commit()
            flash("spread saved for %s @ %s" % ( game.away_team, game.home_team )  , 'info')
        
    games = Schedule.query.filter(Schedule.week==getCurrentWeek()).order_by(Schedule.week_game_id)
    
    form = AddSpread()
    form.week.data = getCurrentWeek()

    return render_template('admin-addspreads.html',
        games = games,
        form = form,
        username = getUserName(),
        current_week = getCurrentWeek(),
        current_admin_pool = getCurrentAdminPool(),
        poolAdmin = current_user.poolAdmin,
        admin_pools=getCommissionerPools())


###############################################################################
# admin pool
###############################################################################    
@app.route('/admin-pool')
def adminPool():
    
    if getUserName() == None:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        if 'pool' in request.args:
            session['current_admin_pool_id'] = request.args.get('pool')
    
    players = []
    current_admin_pool = getCurrentAdminPool()
    if current_admin_pool is not None:
        for player, poolplayer in db.session.query(Player, PoolPlayer).join(PoolPlayer).filter_by(pool_id = current_admin_pool['id']):
            players.append({'id' : poolplayer.id, 
                            'accepted' : poolplayer.accepted, 
                            'suspended' : poolplayer.suspended,
                            'name' : poolplayer.nickName,
                            'email' : player.email})

    form = PoolAddPlayer(request.form)
    form.poolId.data = current_admin_pool

    return render_template('admin-pool.html',
        username = getUserName(), 
        current_admin_pool = current_admin_pool,
        form = form,
        players = players,
        poolAdmin = current_user.poolAdmin,
        admin_pools=getCommissionerPools())
    
###############################################################################
# admin pool add player
###############################################################################    
@app.route('/admin-pool-add-player',  methods=['POST'])
def adminPoolAddPlayer():
    if getUserName() == None:
        return redirect(url_for('login'))
    
    form = PoolAddPlayer(request.form)
    if form.validate() is False:
        return redirect(url_for('do_error', messages="player does not exists")) 
    
    current_admin_pool = getCurrentAdminPool()
        
    if 'current_admin_pool_id' in session:
        newPassword = None
        player = Player.query.filter_by(email=form.email.data.lower()).first()
        if player is None:
            newPassword = str(uuid.uuid4().get_hex().upper()[0:6])
            player = Player(email=form.email.data.lower(), password = bcrypt.generate_password_hash(newPassword))
            db.session.add(player)
            db.session.commit()
            db.session.flush

        poolPlayer = PoolPlayer(pool_id=session['current_admin_pool_id'], nickName = form.nickName.data, player_id=player.id)
        if poolPlayer.id is not None:
            flash('Playe with email=%s alread exists in pool' % player.email)
        else:
            db.session.add(poolPlayer)
        db.session.commit()
        
        #send email
        if newPassword:
            send_email(subject = 'FootBall Pool Invitation',
                        sender = 'noreply@pickemballer.com',
                        recipients = player.email,
                        text_body = render_template('email-pool-invite.txt', commissioner_name = current_user.name(), player_name = player.name(), pool_name = current_admin_pool['name'], password = newPassword ),
                        html_body='')
        else:
            send_email(subject = 'FootBall Pool Invitation',
                        sender = 'noreply@pickemballer.com',
                        recipients = player.email,
                        text_body = render_template('email-pool-invite.txt', commissioner_name = current_user.name(), player_name = player.name(), pool_name = current_admin_pool['name'], password = None ),
                        html_body='')

        return redirect(url_for('adminPool'))
        
    else:
        return redirect(url_for('do_error', messages='No curent pool id')) 

###############################################################################
# erros
###############################################################################    
@app.route('/error')
def do_error():
    messages = request.args.get('messages') 
    return "ERROR: %s" % messages
