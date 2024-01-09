import json
import os
from webapp.main.app import parse_cv
import pytest
from unittest.mock import patch, Mock
from io import StringIO


@pytest.mark.parametrize('filename,expected', [
    ('EXAMPLE_JSON', 'Rosie Miller\nPittsburgh, PA 15201\n(555) 555-5555\nexample@example.com'),
    ('EXAMPLE_TXT', ['Rosie Miller', 'Pittsburgh, PA 15201', '(555) 555-5555', 'example@example.com'])
])
def test_parse_cv(filename, expected):
    result = parse_cv(os.getenv(filename), 'personal')
    assert result == expected


def test_parse_cv_missing_field():
    expected = parse_cv(os.getenv('EXAMPLE_JSON'), 'empty')
    assert expected == ''


def test_list_endpoints(client):
    response = client.get("/")
    assert json.loads(response.data) == {'endpoints': ['personal', 'experience', 'skills', 'education', 'achievements']}


def test_get_cv_label_content_existing(client):

    response = client.get("/personal")
    assert json.loads(response.data) == {
        'result': ['Rosie Miller', 'Pittsburgh, PA 15201', '(555) 555-5555', 'example@example.com']}
    assert response.status_code == 200


def test_get_cv_label_content_missing(client):
    response = client.get("/empty")
    assert json.loads(response.data) == {
        'error': "Content for endpoint 'empty' not found"}
    assert response.status_code == 404


FILE_CONTENT = """PERSONAL DETAILS
Rosie Miller
Pittsburgh, PA 15201
(555) 555-5555
example@example.com
"""


@patch('builtins.open')
@patch('os.path.exists', Mock(return_value=True))
def test_mock_parse(mock_open):
    mock_open.return_value.__enter__.return_value = StringIO(FILE_CONTENT)
    result = parse_cv('/test/file', 'personal')
    assert result == ['Rosie Miller', 'Pittsburgh, PA 15201', '(555) 555-5555', 'example@example.com']
