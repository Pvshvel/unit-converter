from typing import TypeVar

from app.enums import LengthUnit, TemperatureUnit, WeightUnit


UnitType = TypeVar('UnitType', LengthUnit, TemperatureUnit, WeightUnit)
