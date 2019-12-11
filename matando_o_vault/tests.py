import json

import falcon
import msgpack
import pytest
from falcon import testing
from mixer.backend.sqlalchemy import Mixer

from matando_o_vault.app import get_app, db_connection
from matando_o_vault.models import Question, QuestionSchema


@pytest.fixture
def client():
    return testing.TestClient(get_app())


@pytest.fixture
def mixer():
    return Mixer(session=db_connection.get(), commit=True)


def test_list_quests_using_json_api(client, mixer):
    question = QuestionSchema().dump(mixer.blend(Question))

    response = client.simulate_get('/api/v1/quests')


    assert response.status == falcon.HTTP_OK
    assert question in response.json


def test_list_quests_using_mpack_api(client, mixer):
    question = QuestionSchema().dump(mixer.blend(Question))

    response = client.simulate_get('/api/v2/quests')

    questions = msgpack.unpackb(response.content, raw=False)

    assert response.status == falcon.HTTP_OK
    assert question in questions
