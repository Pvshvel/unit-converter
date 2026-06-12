from typing import Generic, Callable


from app.enums import LengthUnit, TemperatureUnit, WeightUnit
from app.unit_types import UnitType
from app.constants import (
    GRAM_CONVERTED_TO_WEIGHT_UNITS,
    CM_CONVERTED_TO_LENGTH_UNITS,
    CELSIUS_CONVERTED_TO_TEMPERATURE_UNITS,
    TO_CELSIUS,
    FROM_CELSIUS,
)
from app.exceptions import ValidationException


class UnitConverter(Generic[UnitType]):
    def __init__(
        self, base_unit: UnitType, converted_units_to_base_unit: dict[UnitType, float]
    ):
        self.base_unit = base_unit
        self.converted_units_to_base_unit = converted_units_to_base_unit

    def _validate_params(
        self, from_unit: UnitType, from_value: float | int, target_unit: UnitType
    ):
        if from_unit not in self.converted_units_to_base_unit:
            raise ValidationException(f'From unit must be {self.base_unit.value} type.')

        if not isinstance(from_value, (float, int)):
            raise ValidationException('Provided value must be a number.')

        if target_unit not in self.converted_units_to_base_unit:
            raise ValidationException(
                f'Target unit must be {self.base_unit.value} type.'
            )

    def get_value_from_unit(self, unit: UnitType) -> float:
        value = self.converted_units_to_base_unit.get(unit)
        if value is None:
            raise ValidationException(f'Value for unit: {unit.value} is not found.')

        return value

    def convert_to_base_unit(self, from_unit: UnitType, from_value: float) -> float:
        return (
            self.get_value_from_unit(self.base_unit)
            * from_value
            / self.get_value_from_unit(from_unit)
        )

    def convert_to_target_unit(self, target_unit: UnitType, from_value: float) -> float:
        return (
            from_value
            * self.get_value_from_unit(target_unit)
            / self.get_value_from_unit(self.base_unit)
        )

    def convert(
        self, from_unit: UnitType, from_value: float | int, target_unit: UnitType
    ) -> float:
        self._validate_params(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        value_in_base_unit = self.convert_to_base_unit(from_unit, from_value)
        return self.convert_to_target_unit(target_unit, value_in_base_unit)


class WeightConverter(UnitConverter[WeightUnit]):
    def _validate_params(
        self, from_unit: UnitType, from_value: float | int, target_unit: UnitType
    ):
        super()._validate_params(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        if from_value < 0:
            raise ValidationException('Provided value must be positive.')


class LengthConverter(UnitConverter[LengthUnit]):
    def _validate_params(
        self, from_unit: UnitType, from_value: float | int, target_unit: UnitType
    ):
        super()._validate_params(
            from_unit=from_unit, from_value=from_value, target_unit=target_unit
        )
        if from_value < 0:
            raise ValidationException('Provided value must be positive.')


class TemperatureConverter(UnitConverter[TemperatureUnit]):
    def __init__(
        self,
        base_unit: UnitType,
        converted_units_to_base_unit: dict[UnitType, float],
        conversion_formulas_to_base_unit: dict[str, Callable],
        conversion_formulas_from_base_unit: dict[str, Callable],
    ):
        super().__init__(
            base_unit=base_unit,
            converted_units_to_base_unit=converted_units_to_base_unit,
        )
        self.conversion_formulas_to_base_unit = conversion_formulas_to_base_unit
        self.conversion_formulas_from_base_unit = conversion_formulas_from_base_unit

    def convert_to_base_unit(self, from_unit: UnitType, from_value: float) -> float:
        return self.conversion_formulas_to_base_unit.get(from_unit)(from_value)

    def convert_to_target_unit(self, target_unit: UnitType, from_value: float) -> float:
        return self.conversion_formulas_from_base_unit.get(target_unit)(from_value)


weight_converter = WeightConverter(
    base_unit=WeightUnit.GRAM,
    converted_units_to_base_unit=GRAM_CONVERTED_TO_WEIGHT_UNITS,
)

length_converter = LengthConverter(
    base_unit=LengthUnit.CENTIMETER,
    converted_units_to_base_unit=CM_CONVERTED_TO_LENGTH_UNITS,
)

temperature_converted = TemperatureConverter(
    base_unit=TemperatureUnit.CELSIUS,
    converted_units_to_base_unit=CELSIUS_CONVERTED_TO_TEMPERATURE_UNITS,
    conversion_formulas_to_base_unit=TO_CELSIUS,
    conversion_formulas_from_base_unit=FROM_CELSIUS,
)
