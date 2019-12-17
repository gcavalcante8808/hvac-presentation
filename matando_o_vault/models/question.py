from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import Column, Integer, DECIMAL, String, DateTime

from utils.db import Base
import datetime


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question_text = Column(String(length=100), nullable=True)
    pub_date = Column(DateTime, default=datetime.datetime.now())



class QuestionSchema(ModelSchema):
    class Meta:
        model = Question
