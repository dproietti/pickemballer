from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
pool_player = Table('pool_player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('pool_id', Integer),
    Column('player_id', Integer),
    Column('commissioner', Boolean, default=ColumnDefault(False)),
    Column('accepted', Boolean, default=ColumnDefault(False)),
    Column('suspended', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pool_player'].columns['pool_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pool_player'].columns['pool_id'].drop()
