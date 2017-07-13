from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bookmarks import app

DATABASE_URL = 'postgresql://{}:{}@{}/{}'.format(
    app.config['DATABASE_USERNAME'],
    app.config['DATABASE_PASSWORD'],
    app.config['DATABASE_HOST'],
    app.config['DATABASE_NAME']
)

engine = create_engine(DATABASE_URL, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import bookmarks.models
    Base.metadata.create_all(bind=engine)
