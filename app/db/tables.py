from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.core import Base


class Respondent(Base):
    __tablename__ = 'respondents'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    respondent_id = Column(ForeignKey('respondents.id'))
    form_id = Column(ForeignKey('forms.id'))
    answer = Column(JSON)


class Form(Base):
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    form = Column(JSON)
    active = Column(Boolean, default=True)
    count = Column(Integer)
