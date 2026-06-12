import pytest
import re

from app.converter import weight_converter
from app.unit_types import WeightUnit, LengthUnit
from app.constants import GRAM_CONVERTED_TO_WEIGHT_UNITS
from app.exceptions import ValidationException


# 1. Converter Types
def test_check_weight_converter_base_unit():
    assert weight_converter.base_unit == WeightUnit.GRAM


def test_check_weight_converter_converted_units():
    assert (
        weight_converter.converted_units_to_base_unit == GRAM_CONVERTED_TO_WEIGHT_UNITS
    )


def test_check_weight_corresponding_converted_units():
    units = list(WeightUnit)
    assert all(unit in units for unit in weight_converter.converted_units_to_base_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (1, None, WeightUnit.GRAM),
        ('String', 2, WeightUnit.GRAM),
        (1.1, 1, WeightUnit.GRAM),
        (LengthUnit.YARD, 1, WeightUnit.GRAM),
    ],
)
def test_weight_invalid_from_unit_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match=r'From unit must be'):
        weight_converter.convert(from_unit, from_value, target_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (WeightUnit.GRAM, 1, None),
        (WeightUnit.GRAM, 1, 1),
        (WeightUnit.GRAM, 2, 'String'),
        (WeightUnit.GRAM, 1, 1.1),
        (WeightUnit.GRAM, 1, LengthUnit.YARD),
    ],
)
def test_weight_invalid_target_unit_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match=re.escape('unit must be')):
        weight_converter.convert(from_unit, from_value, target_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (WeightUnit.GRAM, WeightUnit.GRAM, WeightUnit.GRAM),
        (WeightUnit.GRAM, 'String', WeightUnit.GRAM),
        (WeightUnit.GRAM, None, WeightUnit.GRAM),
    ],
)
def test_weight_invalid_from_value_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match='Provided value must be a number.'):
        weight_converter.convert(from_unit, from_value, target_unit)


def test_weight_negative_from_value():
    with pytest.raises(ValidationException, match='Provided value must be positive.'):
        weight_converter.convert(WeightUnit.GRAM, -1, WeightUnit.GRAM)


# 2. Conversion
@pytest.mark.parametrize(
    'from_unit , from_value , target_unit , expected_result',
    [
        (WeightUnit.GRAM, 1, unit, GRAM_CONVERTED_TO_WEIGHT_UNITS.get(unit))
        for unit in WeightUnit
    ],
)
def test_weight_converter_success_conversion_to_base(
    from_unit, from_value, target_unit, expected_result
):
    assert (
        weight_converter.convert(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        == expected_result
    )


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit , expected_result',
    [
        (WeightUnit.GRAM, 145.5, WeightUnit.MILLIGRAM, 145500),
        (WeightUnit.KILOGRAM, 768.4, WeightUnit.POUND, 1694.0338499809436),
        (WeightUnit.OUNCE, 900, WeightUnit.GRAM, 25514.543289675115),
        (WeightUnit.POUND, 12345.54321, WeightUnit.MILLIGRAM, 5599838163.015876),
        (WeightUnit.MILLIGRAM, 1, WeightUnit.KILOGRAM, 1e-6),
    ],
)
def test_weight_converter_success_conversion(
    from_unit, from_value, target_unit, expected_result
):
    assert (
        weight_converter.convert(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        == expected_result
    )


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit ',
    [
        (WeightUnit.GRAM, 145.5, WeightUnit.MILLIGRAM),
        (WeightUnit.KILOGRAM, 768.4, WeightUnit.POUND),
        (WeightUnit.OUNCE, 900, WeightUnit.GRAM),
        (WeightUnit.POUND, 12345.54321, WeightUnit.MILLIGRAM),
        (WeightUnit.MILLIGRAM, 1, WeightUnit.KILOGRAM),
    ],
)
def test_weight_converter_success_reverse_conversion(
    from_unit, from_value, target_unit
):
    conversion_result = weight_converter.convert(
        from_unit=from_unit, from_value=from_value, target_unit=target_unit
    )
    original_from_value = weight_converter.convert(
        from_unit=target_unit, from_value=conversion_result, target_unit=from_unit
    )

    assert original_from_value == from_value
