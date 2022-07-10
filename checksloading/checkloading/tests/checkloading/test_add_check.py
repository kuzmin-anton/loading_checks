import pytest
import json

from django.urls import reverse
from enum import Enum


class ErrorMessage(Enum):
    """Possible error messages"""
    REQUIRED_FIELD = "Обязательное поле."
    FIELD_CANNOT_BE_EMPTY = "Это поле не может быть пустым."
    INCORRECT_DATETIME = "Неправильный формат datetime. Используйте один из этих форматов:  YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
    INVALID_LENGTH = "Убедитесь, что это значение содержит не более 20 символов."
    STARTDATE_MORE_ENDDATE = "Начальная дата и время должны быть меньше конечной."
    INCORRECT_NUMBER = "Введите правильное число."


@pytest.mark.django_db
def test_add_check_with_valid_data(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = response.data

    assert data["customer_id"] == payload["customer_id"]
    assert data["check_number"] == payload["check_number"]
    assert data["pos_id"] == payload["pos_id"]
    assert data["check_issuance_time"] == payload["check_issuance_time"
                                                  ]
    assert data["total"] == payload["total"]
    assert response.status_code == 201


@pytest.mark.django_db
def test_add_check_with_empty_json(client):
    payload = dict()
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['customer_id'][0] == ErrorMessage.REQUIRED_FIELD.value
    assert data['check_number'][0] == ErrorMessage.REQUIRED_FIELD.value
    assert data['pos_id'][0] == ErrorMessage.REQUIRED_FIELD.value
    assert data['check_issuance_time'][0] == ErrorMessage.REQUIRED_FIELD.value
    assert data['total'][0] == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_add_check_without_customer_id(client):
    payload = dict(
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['customer_id'][0] == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_add_check_without_check_number(client):
    payload = dict(
        customer_id="UID_15",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['check_number'][0] == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_add_check_without_pos_id(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['pos_id'][0] == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_add_check_without_check_issuance_time(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['check_issuance_time'][0] == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_add_check_without_total(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00"
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['total'][0] == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_add_check_with_empty_fields(client):
    payload = dict(
        customer_id="",
        check_number="",
        pos_id="",
        check_issuance_time="",
        total=""
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['customer_id'][0] == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value
    assert data['check_number'][0] == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value
    assert data['pos_id'][0] == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value
    assert data['check_issuance_time'][0] == ErrorMessage.INCORRECT_DATETIME.value
    assert data['total'][0] == ErrorMessage.INCORRECT_NUMBER.value


@pytest.mark.django_db
def test_add_check_with_empty_customer_id(client):
    payload = dict(
        customer_id="",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['customer_id'][0] == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value


@pytest.mark.django_db
def test_add_check_with_empty_check_number(client):
    payload = dict(
        customer_id="UID_15",
        check_number="",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['check_number'][0] == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value


@pytest.mark.django_db
def test_add_check_with_empty_pos_id(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['pos_id'][0] == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value


@pytest.mark.django_db
def test_add_check_with_empty_check_issuance_time(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['check_issuance_time'][0] == ErrorMessage.INCORRECT_DATETIME.value


@pytest.mark.django_db
def test_add_check_with_empty_total(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=""
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['total'][0] == ErrorMessage.INCORRECT_NUMBER.value


@pytest.mark.django_db
def test_add_check_with_invalid_length_customer_id(client):
    payload = dict(
        customer_id="123456789012345678901",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['customer_id'][0] == ErrorMessage.INVALID_LENGTH.value


@pytest.mark.django_db
def test_add_check_with_invalid_length_check_number(client):
    payload = dict(
        customer_id="UID_15",
        check_number="123456789012345678901",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['check_number'][0] == ErrorMessage.INVALID_LENGTH.value


@pytest.mark.django_db
def test_add_check_with_invalid_length_pos_id(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="123456789012345678901",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['pos_id'][0] == ErrorMessage.INVALID_LENGTH.value


@pytest.mark.django_db
def test_add_check_with_invalid_format_check_issuance_time(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="1 января 2022",
        total=10000
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['check_issuance_time'][0] == ErrorMessage.INCORRECT_DATETIME.value


@pytest.mark.django_db
def test_add_check_with_invalid_format_total(client):
    payload = dict(
        customer_id="UID_15",
        check_number="C53150",
        pos_id="POS_253217",
        check_issuance_time="2022-07-10T00:00:00+03:00",
        total="10000 рублей"
    )
    url = reverse('add_check')
    response = client.post(url, payload)
    data = json.loads(response.content.decode('utf-8'))

    assert response.status_code == 400
    assert data['total'][0] == ErrorMessage.INCORRECT_NUMBER.value
