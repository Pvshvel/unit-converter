from typing import Callable

from app.enums import WeightUnit, LengthUnit, TemperatureUnit

GRAM_CONVERTED_TO_WEIGHT_UNITS: dict[WeightUnit, float] = {
    WeightUnit.MILLIGRAM: 1000,
    WeightUnit.GRAM: 1,
    WeightUnit.KILOGRAM: 0.001,
    WeightUnit.OUNCE: 0.035274,
    WeightUnit.POUND: 0.0022046249999752,
}

CM_CONVERTED_TO_LENGTH_UNITS: dict[LengthUnit, float] = {
    LengthUnit.MILLIMETER: 10,
    LengthUnit.CENTIMETER: 1,
    LengthUnit.METER: 0.01,
    LengthUnit.KILOMETER: 1e-5,
    LengthUnit.INCH: 0.393700787,
    LengthUnit.FOOT: 0.032808399,
    LengthUnit.YARD: 0.010936133,
    LengthUnit.MILE: 0.0000062137119,
}

CELSIUS_CONVERTED_TO_TEMPERATURE_UNITS: dict[TemperatureUnit, float] = {
    TemperatureUnit.CELSIUS: 1,
    TemperatureUnit.FAHRENHEIT: 33.8,
    TemperatureUnit.KELVIN: 274.15,
}


TO_CELSIUS: dict[TemperatureUnit, Callable] = {
    TemperatureUnit.CELSIUS: lambda c: c,
    TemperatureUnit.KELVIN: lambda k: k - 273.15,
    TemperatureUnit.FAHRENHEIT: lambda f: (f - 32) * 5 / 9,
}

FROM_CELSIUS: dict[TemperatureUnit, Callable] = {
    TemperatureUnit.CELSIUS: lambda c: c,
    TemperatureUnit.KELVIN: lambda c: c + 273.15,
    TemperatureUnit.FAHRENHEIT: lambda c: (c * 9 / 5) + 32,
}
