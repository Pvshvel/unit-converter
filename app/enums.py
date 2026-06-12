from enum import StrEnum


class LengthUnit(StrEnum):
    MILLIMETER = 'MILLIMETER'
    CENTIMETER = 'CENTIMETER'
    METER = 'METER'
    KILOMETER = 'KILOMETER'
    INCH = 'INCH'
    FOOT = 'FOOT'
    YARD = 'YARD'
    MILE = 'MILE'


class WeightUnit(StrEnum):
    MILLIGRAM = 'MILLIGRAM'
    GRAM = 'GRAM'
    KILOGRAM = 'KILOGRAM'
    OUNCE = 'OUNCE'
    POUND = 'POUND'


class TemperatureUnit(StrEnum):
    CELSIUS = 'CELSIUS'
    FAHRENHEIT = 'FAHRENHEIT'
    KELVIN = 'KELVIN'
