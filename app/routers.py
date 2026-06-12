from typing import Annotated
from fastapi import APIRouter, Query
import logging

from app.schemas import ConversionUnitResponse, ConversionUnit
from app.enums import WeightUnit, LengthUnit, TemperatureUnit
from app.converter import temperature_converted, length_converter, weight_converter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/convert', tags=['Unit conversion'])


@router.get('/weight', response_model=ConversionUnitResponse[WeightUnit])
async def convert_weight(
    unit: Annotated[ConversionUnit[WeightUnit], Query()],
) -> dict[str, WeightUnit | float]:
    logger.info('convert_weight start')
    converted_value = weight_converter.convert(
        unit.from_unit, unit.from_value, unit.target_unit
    )
    logger.info('convert_weight finished')
    return dict(
        from_unit=unit.from_unit,
        from_value=unit.from_value,
        target_unit=unit.target_unit,
        converted_value=converted_value,
    )


@router.get('/length', response_model=ConversionUnitResponse[LengthUnit])
async def convert_length(
    unit: Annotated[ConversionUnit[LengthUnit], Query()],
) -> dict[str, LengthUnit | float]:
    logger.info('convert_length start')
    converted_value = length_converter.convert(
        unit.from_unit, unit.from_value, unit.target_unit
    )
    logger.info('convert_length finished')
    return dict(
        from_unit=unit.from_unit,
        from_value=unit.from_value,
        target_unit=unit.target_unit,
        converted_value=converted_value,
    )


@router.get('/temperature', response_model=ConversionUnitResponse[TemperatureUnit])
async def convert_temperature(
    unit: Annotated[ConversionUnit[TemperatureUnit], Query()],
) -> dict[str, TemperatureUnit | float]:
    logger.info('convert_temperature start')
    converted_value = temperature_converted.convert(
        unit.from_unit, unit.from_value, unit.target_unit
    )
    logger.info('convert_temperature finished')
    return dict(
        from_unit=unit.from_unit,
        from_value=unit.from_value,
        target_unit=unit.target_unit,
        converted_value=converted_value,
    )
