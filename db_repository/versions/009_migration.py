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
    Column('home_name', String(length=10)),
    Column('home_city', String(length=15)),
    Column('away_team', Integer),
    Column('away_name', String(length=10)),
    Column('away_city', String(length=15)),
    Column('home_line', Integer),
    Column('away_line', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['schedule'].columns['away_city'].create()
    post_meta.tables['schedule'].columns['away_name'].create()
    post_meta.tables['schedule'].columns['home_city'].create()
    post_meta.tables['schedule'].columns['home_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['schedule'].columns['away_city'].drop()
    post_meta.tables['schedule'].columns['away_name'].drop()
    post_meta.tables['schedule'].columns['home_city'].drop()
    post_meta.tables['schedule'].columns['home_name'].drop()
