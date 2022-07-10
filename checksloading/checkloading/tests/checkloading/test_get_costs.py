import pytest
from enum import Enum

from django.urls import reverse


class ErrorMessage(Enum):
    """Possible error messages"""
    REQUIRED_FIELD = "Обязательное поле."
    FIELD_CANNOT_BE_EMPTY = "Это поле не может быть пустым."
    INCORRECT_DATETIME = "Неправильный формат datetime. Используйте один из этих форматов:  YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
    INVALID_LENGTH = "Убедитесь, что это значение содержит не более 20 символов."
    STARTDATE_MORE_ENDDATE = "Начальная дата и время должны быть меньше конечной."


@pytest.mark.django_db
def test_get_costs_with_valid_data(client):
    payload = dict(
        customer_id="UID_15",
        start_date="2022-07-01T00:00:00",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    data = response.content_type
    print('\n', data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_costs_without_query_params(client):
    payload = dict()
    url = reverse('get_costs')
    response = client.get(url, payload)
    customer_id = response.data['customer_id'][0]
    start_date = response.data['start_date'][0]
    end_date = response.data['end_date'][0]

    assert response.status_code == 400
    assert customer_id == ErrorMessage.REQUIRED_FIELD.value
    assert start_date == ErrorMessage.REQUIRED_FIELD.value
    assert end_date == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_get_costs_without_customer_id(client):
    payload = dict(
        start_date="2022-07-01T00:00:00",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    customer_id = response.data['customer_id'][0]

    assert response.status_code == 400
    assert customer_id == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_get_costs_without_start_date(client):
    payload = dict(
        customer_id="UID_15",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    start_date = response.data['start_date'][0]

    assert response.status_code == 400
    assert start_date == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_get_costs_without_end_date(client):
    payload = dict(
        customer_id="UID_15",
        start_date="2022-07-01T00:00:00",
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    end_date = response.data['end_date'][0]

    assert response.status_code == 400
    assert end_date == ErrorMessage.REQUIRED_FIELD.value


@pytest.mark.django_db
def test_get_costs_with_empty_customer_id(client):
    payload = dict(
        customer_id="",
        start_date="2022-07-01T00:00:00",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    customer_id = response.data['customer_id'][0]

    assert response.status_code == 400
    assert customer_id == ErrorMessage.FIELD_CANNOT_BE_EMPTY.value


@pytest.mark.django_db
def test_get_costs_with_empty_start_date(client):
    payload = dict(
        customer_id="UID_15",
        start_date="",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    start_date = response.data['start_date'][0]

    assert response.status_code == 400
    assert start_date == ErrorMessage.INCORRECT_DATETIME.value


@pytest.mark.django_db
def test_get_costs_with_empty_end_date(client):
    payload = dict(
        customer_id="UID_15",
        start_date="2022-07-01T00:00:00",
        end_date=""
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    end_date = response.data['end_date'][0]

    assert response.status_code == 400
    assert end_date == ErrorMessage.INCORRECT_DATETIME.value


@pytest.mark.django_db
def test_get_costs_with_invalid_length_customer_id(client):
    payload = dict(
        customer_id="123456789012345678901",
        start_date="2022-07-01T00:00:00",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    customer_id = response.data['customer_id'][0]

    assert response.status_code == 400
    assert customer_id == ErrorMessage.INVALID_LENGTH.value


@pytest.mark.django_db
def test_get_costs_with_invalid_start_date(client):
    payload = dict(
        customer_id="UID_15",
        start_date="01-07-2022",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    start_date = response.data['start_date'][0]

    assert response.status_code == 400
    assert start_date == ErrorMessage.INCORRECT_DATETIME.value


@pytest.mark.django_db
def test_get_costs_with_invalid_end_date(client):
    payload = dict(
        customer_id="UID_15",
        start_date="2022-01-01T00:00:00",
        end_date="2022-02-31T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    end_date = response.data['end_date'][0]

    assert response.status_code == 400
    assert end_date == ErrorMessage.INCORRECT_DATETIME.value


@pytest.mark.django_db
def test_get_costs_with_start_date_greater_end_date(client):
    payload = dict(
        customer_id="UID_15",
        start_date="2022-07-12T00:00:00",
        end_date="2022-07-11T00:00:00"
    )
    url = reverse('get_costs')
    response = client.get(url, payload)
    start_date = response.data['end_date'][0]

    assert response.status_code == 400
    assert start_date == ErrorMessage.STARTDATE_MORE_ENDDATE.value
