from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('pool_id', INTEGER),
    Column('player_id', INTEGER),
    Column('week', INTEGER),
    Column('game_1', BOOLEAN),
    Column('game_2', BOOLEAN),
    Column('game_3', BOOLEAN),
    Column('game_4', BOOLEAN),
    Column('game_5', BOOLEAN),
    Column('game_6', BOOLEAN),
    Column('game_7', BOOLEAN),
    Column('game_8', BOOLEAN),
    Column('game_9', BOOLEAN),
    Column('game_10', BOOLEAN),
    Column('game_11', BOOLEAN),
    Column('game_12', BOOLEAN),
    Column('game_13', BOOLEAN),
    Column('game_14', BOOLEAN),
    Column('game_15', BOOLEAN),
    Column('game_16', BOOLEAN),
    Column('tieBreaker', INTEGER),
    Column('showPicks', BOOLEAN),
)

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
    Column('showPicks', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['pics'].columns['showPicks'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['pics'].columns['showPicks'].drop()
