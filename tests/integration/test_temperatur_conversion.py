import pytest
from fastapi.testclient import TestClient
from fastapi import status


URL = '/convert/temperature'


@pytest.mark.parametrize(
    'from_unit, from_value, target_unit, expected_result',
    [
        ('CELSIUS', 36.6, 'KELVIN', 309.75),
        ('FAHRENHEIT', 123.321, 'CELSIUS', 50.73388889),
        ('KELVIN', 0.05, 'FAHRENHEIT', -459.58),
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

    assert expected_result == pytest.approx(
        conversion_data['converted_value'], rel=1e-4
    )


def test_conversion_large_value(test_client: TestClient):
    response = test_client.get(
        URL,
        params={
            'from_unit': 'CELSIUS',
            'from_value': 123456789123456789.1234556789,
            'target_unit': 'FAHRENHEIT',
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'from_unit, from_value, target_unit',
    [
        ('CM', 1, 'KM'),
        (None, 0, None),
        (123, 123, 123),
        ('MILE', 'MILE', 'MILE'),
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
