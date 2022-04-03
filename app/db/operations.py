from typing import Dict
from app.db.tables import Answer, Base, Respondent, Form
from app.db.core import engine, Session
from app.questions import questions
import json
from sqlalchemy import update


def init_db():
    Base.metadata.create_all(engine, checkfirst=True)
    create_form(questions)


def create_form(form: dict):
    with Session() as session:
        if session.query(Form.id).filter_by(form=form).first() is None:
            form = Form(form=form, count=len(form))
            session.add(form)
            session.commit()


def create_respondent(message):
    with Session() as session:
        if session.query(Respondent.id).filter_by(id=message.from_user.id).first() is None:
            respondent = Respondent(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            session.add(respondent)
            session.commit()


def create_answer(respondent_id: int, form_id: int):
    with Session() as session:
        if session.query(Answer.id).filter(
            Answer.respondent_id.like(respondent_id),
            Answer.form_id.like(form_id)
        ).first() is None:
            answer_dict, count = {}, session.query(
                Form.count).filter_by(id=form_id).first()[0]
            for i in range(0, count):
                answer_dict[i] = None
            answer = Answer(
                respondent_id=respondent_id,
                form_id=form_id,
                answer=answer_dict
            )
            session.add(answer)
            session.commit()


def update_answer(respondent_id: int, form_id: int, answer: Dict[int, int]):
    with Session() as session:
        _answer = session.query(Answer.answer).filter(
            Answer.respondent_id.like(respondent_id)
        ).first()[0]
        _answer = {**_answer, **answer}

        session.query(Answer).filter(Answer.respondent_id==respondent_id).update({'answer': _answer})

        # session.query(Answer.answer).filter(
        #     Answer.respondent_id.like(respondent_id)
        # ).update({Answer.answer: json.dumps(_answer)})

        # session.flush()
        session.commit()


def get_form(form_id: int):
    with Session() as session:
        form = session.query(Form.form).filter_by(id=form_id).first()[0]
    return form


def get_answer(answer_id: int, current_form_id: int):
    with Session() as session:
        answer = session.query(Answer.answer).filter(
            Answer.respondent_id.like(answer_id),
            Answer.form_id.like(current_form_id)
        ).first()[0]
    return answer


def get_question(form_id: int, respondent_id: int, question_index: str):
    with Session() as session:
        form = get_form(form_id)
        question = list(form.items())[int(question_index)]
    return question
