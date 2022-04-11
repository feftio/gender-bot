from typing import Dict, List
from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from sqlalchemy.exc import NoResultFound
from app.db.core import Base, Session
from app.db.exceptions import *


class Respondent(Base):
    __tablename__ = 'respondents'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    @classmethod
    def create(cls, respondent_id: int, username: str, first_name: str, last_name: str):
        with Session() as session:
            if session.query(Respondent.id).filter_by(id=respondent_id).first() is None:
                respondent = Respondent(
                    id=respondent_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(respondent)
                session.commit()


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    respondent_id = Column(ForeignKey('respondents.id'))
    form_id = Column(ForeignKey('forms.id'))
    body = Column(JSON)

    @classmethod
    def create_empty(cls, respondent_id: int, form_id: int):
        with Session() as session:
            if session.query(Answer.id).filter(
                Answer.respondent_id.like(respondent_id),
                Answer.form_id.like(form_id)
            ).first() is None:
                body = dict(
                    [(i, None) for i in range(Form.get(form_id=form_id).count)])
                answer = Answer(
                    respondent_id=respondent_id,
                    form_id=form_id,
                    body=body
                )
                session.add(answer)
                session.commit()

    @classmethod
    def get(cls, respondent_id: int, form_id: int):
        with Session() as session:
            answer = session.query(Answer).filter(
                Answer.respondent_id.like(respondent_id),
                Answer.form_id.like(form_id)
            ).first()
        return answer

    @classmethod
    def update(cls, respondent_id: int, form_id: int, answer_body: Dict[int, int]):
        with Session() as session:
            answer = session.query(Answer).filter(
                Answer.respondent_id == respondent_id,
                Answer.form_id == form_id
            ).one()
            answer.body = {**answer.body, **answer_body}
            session.commit()

    @classmethod
    def next_question(cls, respondent_id: int, form_id: str):
        answer_body = cls.get(
            respondent_id=respondent_id,
            form_id=form_id
        ).body
        for question_index, variant_index in answer_body.items():
            if variant_index is None:
                question, variants = Form.get_question(
                    form_id=form_id,
                    question_index=question_index
                )
                return (question, variants)
        return 0


class Form(Base):
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    body = Column(JSON)
    active = Column(Boolean)
    count = Column(Integer)

    @classmethod
    def create(cls, name: str, body: Dict[str, List[str]], active: bool = True) -> None:
        with Session() as session:
            if session.query(cls.id).filter_by(name=name).first() is None:
                form = cls(name=name, body=body,
                           active=active, count=len(body))
                session.add(form)
                session.commit()

    @classmethod
    def get(cls, form_id: int):
        with Session() as session:
            try:
                form = session.query(cls).filter_by(id=form_id).one()
            except NoResultFound:
                raise NotFoundTableRow(cls, cls.id, form_id)
        return form

    @classmethod
    def get_by_name(cls, form_name: str):
        with Session() as session:
            try:
                form = session.query(cls).filter_by(name=form_name).one()
            except NoResultFound:
                raise NotFoundTableRow(cls, cls.name, form_name)
        return form

    @classmethod
    def get_question(cls, form_id: int, question_index: int):
        body = cls.get(form_id=form_id).body
        question = tuple(body.items())[int(question_index)]
        return question


if __name__ == '__main__':
    print(Form.get_by_name('Main Form').id)
