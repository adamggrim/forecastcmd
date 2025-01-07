from enum import Enum, auto


class TempScale(Enum):
    """
    Enum for selecting the temperature scale to apply to a forecast.
    
    Attributes:
        CELSIUS: Represents the Celsius temperature scale.
        FAHRENHEIT: Represents the Fahrenheit temperature scale.
    """
    CELSIUS = auto()
    FAHRENHEIT = auto()
