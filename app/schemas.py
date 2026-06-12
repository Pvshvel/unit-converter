from typing import Generic
from pydantic import BaseModel, Field

from app.unit_types import UnitType


class ConversionUnit(BaseModel, Generic[UnitType]):
    from_unit: UnitType
    from_value: float = Field(ge=0)
    target_unit: UnitType


class ConversionUnitResponse(BaseModel, Generic[UnitType]):
    from_unit: UnitType
    from_value: float
    target_unit: UnitType
    converted_value: float
