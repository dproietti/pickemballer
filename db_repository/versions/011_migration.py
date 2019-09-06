from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
pics = Table('pics', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('pool_id', Integer),
    Column('player_id', Integer),
    Column('week', Integer),
    Column('game_1', Boolean),
    Column('game_2', Boolean),
    Column('game_3', Boolean),
    Column('game_4', Boolean),
    Column('game_5', Boolean),
    Column('game_6', Boolean),
    Column('game_7', Boolean),
    Column('game_8', Boolean),
    Column('game_9', Boolean),
    Column('game_10', Boolean),
    Column('game_11', Boolean),
    Column('game_12', Boolean),
    Column('game_13', Boolean),
    Column('game_14', Boolean),
    Column('game_15', Boolean),
    Column('game_16', Boolean),
    Column('tieBreaker', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pics'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pics'].drop()
