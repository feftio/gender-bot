from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from app import config

engine = create_engine(
    url='sqlite:///%s' % config.DB_PATH,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
    echo=True
)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
