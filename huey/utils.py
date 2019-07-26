from airflow.hooks.postgres_hook import PostgresHook
from sqlalchemy.orm.session import sessionmaker

def get_db_session():
    engine = PostgresHook(postgres_conn_id='huey_dev').get_sqlalchemy_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    db_session = Session()
    return db_session
