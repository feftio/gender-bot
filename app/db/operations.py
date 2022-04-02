from app.db.tables import Base, Respondent
from app.db.core import engine, Session


def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)


def create_respondent(message):
    with Session() as session:
        if session.query(Respondent.id).filter_by(id=message.from_user.id).first() is None:
            session.add(Respondent(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                full_name=message.from_user.full_name
            ))
            session.commit()
