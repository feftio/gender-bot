from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from app.db.core import Base


class Respondent(Base):
    __tablename__ = 'respondents'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, full_name={self.full_name})>"


# class Questions(Base):
#     __tablename__ = 'questions'
