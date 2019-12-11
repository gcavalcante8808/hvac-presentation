from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey

from matando_o_vault.utils.db import Base


class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    choice_text = Column(String(length=200))
    votes = Column(Integer, default=0)



class ChoiceSchema(ModelSchema):
    class Meta:
        model = Choice
