from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
schedule = Table('schedule', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('eid', Integer),
    Column('week', Integer),
    Column('start_time', DateTime),
    Column('home_team', Integer),
    Column('away_team', Integer),
)

team = Table('team', post_meta,
    Column('id', String(length=3), primary_key=True, nullable=False),
    Column('city', String(length=15)),
    Column('name', String(length=10)),
    Column('losses', Integer),
    Column('wins', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['schedule'].create()
    post_meta.tables['team'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['schedule'].drop()
    post_meta.tables['team'].drop()
