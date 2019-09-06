from app import db, bcrypt
import datetime
from pytz import timezone

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(10))
    lastname = db.Column(db.String(10))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    authenticated = db.Column(db.Boolean, default=False)
    poolPlayer = db.relationship('PoolPlayer', backref='player')
    poolAdmin = db.Column(db.Boolean, default=False)

    def name(self):
        if self.firstname is not None and self.lastname is not None:
            return '%s %s' % (self.firstname, self.lastname)
        elif self.lastname is not None:
            return self.lastname
        elif self.firstname is not None:
            return self.firstname
        else:
            return self.email.split('@')[0]
            
    def validatePassword(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def setPassword(self, password = None):
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<Player %r, %r, email=%r, id=%r>' % (self.firstname, self.lastname, self.email, self.id)
        
    def is_active(self):
        """True, as all users are active."""
        return self.password is not None

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
        
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
        
class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    commissioner = db.Column(db.Integer, db.ForeignKey('player.id'))
    type = db.Column(db.String(10))
    poolPlayer = db.relationship('PoolPlayer', backref='pool')

class PoolPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_id = db.Column(db.Integer, db.ForeignKey('pool.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    nickName = db.Column(db.String(30))
    commissioner = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean, default=False)
    suspended = db.Column(db.Boolean, default=False)

class Team(db.Model):
    id = db.Column(db.String(3), primary_key=True)
    city = db.Column(db.String(15))
    name = db.Column(db.String(10))
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    ties = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return '<Team id=%r city=%r name-%r>' % (self.id, self.city, self.name)
    
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eid =  db.Column(db.Integer)
    week =  db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_line = db.Column(db.Integer)
    away_line = db.Column(db.Integer)
    over_under = db.Column(db.Integer)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    week_game_id = db.Column(db.Integer)
    
    def atsWinner(self):
        if self.home_score is None:
            return None
        else:
            if self.home_score + self.home_line > self.away_score:
                return 1
            elif self.home_score + self.home_line < self.away_score:
                return 0
            else:
                return None

    def gameStarted(self):
        EST=timezone('US/Eastern')
        gameTimeEST = datetime.datetime(year=self.start_time.year, month=self.start_time.month, day=self.start_time.day, hour=self.start_time.hour, minute=self.start_time.minute, second=self.start_time.second, microsecond=111111, tzinfo=EST)
        dtNow = datetime.datetime.now(EST)
        nowTimeEST = datetime.datetime(year=dtNow.year, month=dtNow.month, day=dtNow.day, hour=dtNow.hour, minute=dtNow.minute, second=dtNow.second, microsecond=111111, tzinfo=EST)
        if nowTimeEST >gameTimeEST:
            return True
        else:
            return False
        
        
class Pics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_id = db.Column(db.Integer, db.ForeignKey('pool.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)   
    week =  db.Column(db.Integer)
    game_1 =  db.Column(db.Boolean)
    game_2 =  db.Column(db.Boolean)
    game_3 =  db.Column(db.Boolean)
    game_4 =  db.Column(db.Boolean)
    game_5 =  db.Column(db.Boolean)
    game_6 =  db.Column(db.Boolean)
    game_7 =  db.Column(db.Boolean)
    game_8 =  db.Column(db.Boolean)
    game_9 =  db.Column(db.Boolean)
    game_10 =  db.Column(db.Boolean)
    game_11 =  db.Column(db.Boolean)
    game_12 =  db.Column(db.Boolean)
    game_13 =  db.Column(db.Boolean)
    game_14 =  db.Column(db.Boolean)
    game_15 =  db.Column(db.Boolean)
    game_16 =  db.Column(db.Boolean)
    tieBreaker = db.Column(db.Integer)
    showPicks = db.Column(db.Boolean)
    wins = db.Column(db.Integer, default=0)
    winner = db.Column(db.Boolean)
    winnerTieBreaker = db.Column(db.Boolean)
    
    
    def __repr__(self):
        return '<Pics id=%r pool_id=%r player_id=%r week=%r>' % (self.id, self.pool_id, self.player_id, self.week)