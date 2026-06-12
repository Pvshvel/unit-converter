import pytest
from fastapi.testclient import TestClient
from fastapi import status


URL = '/convert/weight'


@pytest.mark.parametrize(
    'from_unit, from_value, target_unit, expected_result',
    [
        ('GRAM', 0, 'KILOGRAM', 0),
        ('POUND', 123.321, 'POUND', 123.321),
        ('GRAM', 1000, 'KILOGRAM', 1.0),
        ('KILOGRAM', 0.5, 'GRAM', 500.0),
        ('POUND', 1, 'GRAM', 453.592),
        ('MILLIGRAM', 1000000, 'KILOGRAM', 1),
        ('OUNCE', 16, 'POUND', 1.0),
    ],
)
def test_conversion_success(
    test_client: TestClient, from_unit, from_value, target_unit, expected_result
):
    params = {
        'from_unit': from_unit,
        'from_value': from_value,
        'target_unit': target_unit,
    }

    response = test_client.get(URL, params=params)
    conversion_data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert params['from_unit'] == conversion_data['from_unit']
    assert params['target_unit'] == conversion_data['target_unit']
    assert params['from_value'] == conversion_data['from_value']

    assert conversion_data['converted_value'] == pytest.approx(
        expected_result, rel=1e-4, abs=1e-9
    )


def test_conversion_large_value(test_client: TestClient):
    response = test_client.get(
        URL,
        params={
            'from_unit': 'GRAM',
            'from_value': 123456789123456789.1234556789,
            'target_unit': 'OUNCE',
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'from_unit, from_value, target_unit',
    [
        ('KG', 1, 'OZ'),
        (None, 0, None),
        (123, 123, 123),
        ('GRAM', 'GRAM', 'GRAM'),
    ],
)
def test_conversion_invalid_parameters(
    test_client: TestClient, from_unit, from_value, target_unit
):
    response = test_client.get(
        URL,
        params={
            'from_unit': from_unit,
            'from_value': from_value,
            'target_unit': target_unit,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_conversion_negative_value(test_client: TestClient):
    response = test_client.get(
        URL, params={'from_unit': 'OUNCE', 'from_value': -1, 'target_unit': 'KILOGRAM'}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_conversion_empty_parameters(test_client: TestClient):
    response = test_client.get(URL)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_conversion_wrong_http_method(test_client: TestClient):
    post_response = test_client.post(URL)
    delete_response = test_client.delete(URL)
    patch_response = test_client.patch(URL)

    assert post_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert delete_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert patch_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
