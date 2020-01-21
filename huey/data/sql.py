# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_data.sql.ipynb (unless otherwise specified).

__all__ = ['singleton', 'DB', 'get_db_engine']

# Cell
from ..imports import *

# Cell
def singleton(klass):
    instances = {}

    def get_instance():
        if klass not in instances:
            instances[klass] = klass()
        return instances[klass]
    return get_instance

# Cell
from sqlalchemy.orm.session import sessionmaker

# Cell
@singleton
class DB:
    def __init__(self):
        db_env='huey_dev'
        engine = PostgresHook(postgres_conn_id=db_env).get_sqlalchemy_engine(engine_kwargs=dict(poolclass=NullPool))
        self.engine = engine
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

# Cell
def get_db_engine():
    db = DB()
    return db.engine