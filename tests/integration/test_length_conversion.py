import pytest
from fastapi.testclient import TestClient
from fastapi import status


URL = '/convert/length'


@pytest.mark.parametrize(
    'from_unit, from_value, target_unit, expected_result',
    [
        ('MILLIMETER', 0, 'CENTIMETER', 0),
        ('CENTIMETER', 123.321, 'FOOT', 4.045964567),
        ('METER', 0.05, 'YARD', 0.054680665),
        ('KILOMETER', 0.123, 'MILLIMETER', 123000),
        ('INCH', 8496.463, 'MILE', 0.13409821654),
        ('FOOT', 100956.46445346, 'MILLIMETER', 30771530.365),
        ('YARD', 16, 'KILOMETER', 0.0146304),
        ('MILE', 0.0005, 'METER', 0.804672),
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
            'from_unit': 'MILLIMETER',
            'from_value': 123456789123456789.1234556789,
            'target_unit': 'MILE',
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


def test_conversion_negative_value(test_client: TestClient):
    response = test_client.get(
        URL, params={'from_unit': 'MILE', 'from_value': -1, 'target_unit': 'MILLIMETRE'}
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
