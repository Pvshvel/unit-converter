import pytest
import re

from app.converter import temperature_converted
from app.unit_types import TemperatureUnit, LengthUnit
from app.constants import CELSIUS_CONVERTED_TO_TEMPERATURE_UNITS
from app.exceptions import ValidationException


# 1. Converter Types
def test_check_temperature_converter_base_unit():
    assert temperature_converted.base_unit == TemperatureUnit.CELSIUS


def test_check_temperature_converter_converted_units():
    assert (
        temperature_converted.converted_units_to_base_unit
        == CELSIUS_CONVERTED_TO_TEMPERATURE_UNITS
    )


def test_check_temperature_corresponding_converted_units():
    units = list(TemperatureUnit)
    assert all(
        unit in units for unit in temperature_converted.converted_units_to_base_unit
    )


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (1, None, TemperatureUnit.CELSIUS),
        ('String', 2, TemperatureUnit.CELSIUS),
        (1.1, 1, TemperatureUnit.CELSIUS),
        (LengthUnit.YARD, 1, TemperatureUnit.CELSIUS),
    ],
)
def test_temperature_invalid_from_unit_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match=r'From unit must be'):
        temperature_converted.convert(from_unit, from_value, target_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (TemperatureUnit.CELSIUS, 1, None),
        (TemperatureUnit.CELSIUS, 1, 1),
        (TemperatureUnit.CELSIUS, 2, 'String'),
        (TemperatureUnit.CELSIUS, 1, 1.1),
        (TemperatureUnit.CELSIUS, 1, LengthUnit.KILOMETER),
    ],
)
def test_temperature_invalid_target_unit_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match=re.escape('unit must be')):
        temperature_converted.convert(from_unit, from_value, target_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (
            TemperatureUnit.FAHRENHEIT,
            TemperatureUnit.FAHRENHEIT,
            TemperatureUnit.FAHRENHEIT,
        ),
        (TemperatureUnit.FAHRENHEIT, 'String', TemperatureUnit.FAHRENHEIT),
        (TemperatureUnit.FAHRENHEIT, None, TemperatureUnit.FAHRENHEIT),
    ],
)
def test_length_invalid_from_value_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match='Provided value must be a number.'):
        temperature_converted.convert(from_unit, from_value, target_unit)


# 2. Conversion
@pytest.mark.parametrize(
    'from_unit , from_value , target_unit , expected_result',
    [
        (
            TemperatureUnit.CELSIUS,
            1,
            unit,
            CELSIUS_CONVERTED_TO_TEMPERATURE_UNITS.get(unit),
        )
        for unit in TemperatureUnit
    ],
)
def test_length_converter_success_conversion_to_base(
    from_unit, from_value, target_unit, expected_result
):
    assert (
        temperature_converted.convert(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "from_unit, from_value, target_unit, expected",
    [
        (TemperatureUnit.CELSIUS, 2, TemperatureUnit.FAHRENHEIT, 35.6),
        (TemperatureUnit.CELSIUS, 100, TemperatureUnit.FAHRENHEIT, 212.0),
        (
            TemperatureUnit.CELSIUS,
            -40,
            TemperatureUnit.FAHRENHEIT,
            -40.0,
        ),  # точка пересечения
        (
            TemperatureUnit.CELSIUS,
            -273.15,
            TemperatureUnit.KELVIN,
            0.0,
        ),  # абсолютный ноль
        (TemperatureUnit.FAHRENHEIT, 32, TemperatureUnit.CELSIUS, 0.0),
        (TemperatureUnit.FAHRENHEIT, -40, TemperatureUnit.CELSIUS, -40.0),
        (TemperatureUnit.FAHRENHEIT, 212, TemperatureUnit.KELVIN, 373.15),
        (TemperatureUnit.KELVIN, 0, TemperatureUnit.CELSIUS, -273.15),
        (TemperatureUnit.KELVIN, 373.15, TemperatureUnit.FAHRENHEIT, 212.0),
        (TemperatureUnit.KELVIN, 300, TemperatureUnit.CELSIUS, 26.85),
    ],
)
def test_length_converter_positive(from_unit, from_value, target_unit, expected):
    result = temperature_converted.convert(from_unit, from_value, target_unit)
    assert result == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit ',
    [
        (TemperatureUnit.CELSIUS, 2, TemperatureUnit.FAHRENHEIT),
        (TemperatureUnit.CELSIUS, 100, TemperatureUnit.FAHRENHEIT),
        (TemperatureUnit.CELSIUS, -40, TemperatureUnit.FAHRENHEIT),
        (TemperatureUnit.CELSIUS, -273.15, TemperatureUnit.KELVIN),
        (TemperatureUnit.CELSIUS, 0, TemperatureUnit.CELSIUS),
        (TemperatureUnit.CELSIUS, 37, TemperatureUnit.CELSIUS),
        (TemperatureUnit.CELSIUS, -50, TemperatureUnit.CELSIUS),
        (TemperatureUnit.FAHRENHEIT, 32, TemperatureUnit.CELSIUS),
        (TemperatureUnit.FAHRENHEIT, -40, TemperatureUnit.CELSIUS),
        (TemperatureUnit.FAHRENHEIT, 212, TemperatureUnit.KELVIN),
        (TemperatureUnit.FAHRENHEIT, 98.6, TemperatureUnit.CELSIUS),
        (TemperatureUnit.FAHRENHEIT, -459.67, TemperatureUnit.KELVIN),
        (TemperatureUnit.KELVIN, 0, TemperatureUnit.CELSIUS),
        (TemperatureUnit.KELVIN, 373.15, TemperatureUnit.FAHRENHEIT),
        (TemperatureUnit.KELVIN, 300, TemperatureUnit.CELSIUS),
        (TemperatureUnit.KELVIN, 255.37, TemperatureUnit.FAHRENHEIT),
        (TemperatureUnit.KELVIN, 310.15, TemperatureUnit.CELSIUS),
    ],
)
def test_weight_converter_success_reverse_conversion(
    from_unit, from_value, target_unit
):
    conversion_result = temperature_converted.convert(
        from_unit=from_unit, from_value=from_value, target_unit=target_unit
    )
    original_from_value = temperature_converted.convert(
        from_unit=target_unit, from_value=conversion_result, target_unit=from_unit
    )

    assert pytest.approx(original_from_value, rel=1e-4) == from_value
