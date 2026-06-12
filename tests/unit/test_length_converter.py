import pytest
import re

from app.converter import length_converter
from app.unit_types import WeightUnit, LengthUnit
from app.constants import CM_CONVERTED_TO_LENGTH_UNITS
from app.exceptions import ValidationException


# 1. Converter Types
def test_check_length_converter_base_unit():
    assert length_converter.base_unit == LengthUnit.CENTIMETER


def test_check_length_converter_converted_units():
    assert length_converter.converted_units_to_base_unit == CM_CONVERTED_TO_LENGTH_UNITS


def test_check_length_corresponding_converted_units():
    units = list(LengthUnit)
    assert all(unit in units for unit in length_converter.converted_units_to_base_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (1, None, LengthUnit.CENTIMETER),
        ('String', 2, LengthUnit.CENTIMETER),
        (1.1, 1, LengthUnit.CENTIMETER),
        (WeightUnit.OUNCE, 1, LengthUnit.CENTIMETER),
    ],
)
def test_length_invalid_from_unit_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match=r'From unit must be'):
        length_converter.convert(from_unit, from_value, target_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (LengthUnit.CENTIMETER, 1, None),
        (LengthUnit.CENTIMETER, 1, 1),
        (LengthUnit.CENTIMETER, 2, 'String'),
        (LengthUnit.CENTIMETER, 1, 1.1),
        (LengthUnit.CENTIMETER, 1, WeightUnit.POUND),
    ],
)
def test_length_invalid_target_unit_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match=re.escape('unit must be')):
        length_converter.convert(from_unit, from_value, target_unit)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit',
    [
        (LengthUnit.CENTIMETER, LengthUnit.CENTIMETER, LengthUnit.CENTIMETER),
        (LengthUnit.CENTIMETER, 'String', LengthUnit.CENTIMETER),
        (LengthUnit.CENTIMETER, None, LengthUnit.CENTIMETER),
    ],
)
def test_length_invalid_from_value_types(from_unit, from_value, target_unit):
    with pytest.raises(ValidationException, match='Provided value must be a number.'):
        length_converter.convert(from_unit, from_value, target_unit)


def test_length_negative_from_value():
    with pytest.raises(ValidationException, match='Provided value must be positive.'):
        length_converter.convert(LengthUnit.CENTIMETER, -1, LengthUnit.CENTIMETER)


# 2. Conversion
@pytest.mark.parametrize(
    'from_unit , from_value , target_unit , expected_result',
    [
        (LengthUnit.CENTIMETER, 1, unit, CM_CONVERTED_TO_LENGTH_UNITS.get(unit))
        for unit in LengthUnit
    ],
)
def test_length_converter_success_conversion_to_base(
    from_unit, from_value, target_unit, expected_result
):
    assert (
        length_converter.convert(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "from_unit, from_value, target_unit, expected",
    [
        (LengthUnit.MILLIMETER, 578.91356, LengthUnit.KILOMETER, 0.00057891356),
        (LengthUnit.CENTIMETER, 768.4, LengthUnit.METER, 7.684),
        (LengthUnit.METER, 900, LengthUnit.FOOT, 2880.0),
        (LengthUnit.KILOMETER, 12.5, LengthUnit.MILE, 7.76716),
        (LengthUnit.INCH, 36, LengthUnit.YARD, 0.99943),
        (LengthUnit.FOOT, 5280, LengthUnit.MILE, 1.02526),
        (LengthUnit.YARD, 1760, LengthUnit.MILE, 1.000559),
        (LengthUnit.MILE, 1, LengthUnit.KILOMETER, 1.60934),
    ],
)
def test_length_converter_positive(from_unit, from_value, target_unit, expected):
    result = length_converter.convert(from_unit, from_value, target_unit)
    assert result == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize(
    'from_unit , from_value , target_unit ',
    [
        (LengthUnit.METER, 1, LengthUnit.FOOT),
        (LengthUnit.KILOMETER, 0.5, LengthUnit.MILE),
        (LengthUnit.INCH, 100, LengthUnit.CENTIMETER),
        (LengthUnit.YARD, 3, LengthUnit.METER),
        (LengthUnit.MILE, 2.5, LengthUnit.KILOMETER),
        (LengthUnit.FOOT, 1000, LengthUnit.METER),
    ],
)
def test_weight_converter_success_reverse_conversion(
    from_unit, from_value, target_unit
):
    conversion_result = length_converter.convert(
        from_unit=from_unit, from_value=from_value, target_unit=target_unit
    )
    original_from_value = length_converter.convert(
        from_unit=target_unit, from_value=conversion_result, target_unit=from_unit
    )

    assert pytest.approx(original_from_value, rel=1e-4) == from_value
