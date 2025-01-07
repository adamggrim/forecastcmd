from typing import Optional

from forecastcmd.constants import (
    CELSIUS_INPUTS, 
    ENTER_TEMP_SCALE_PROMPT, 
    FAHRENHEIT_INPUTS
)
from forecastcmd.input_output import (
    ForecastLoop, 
    print_padding, 
    print_wrapped,
    program_exit, 
    prompt_for_temp_scale
)
from forecastcmd.parsing import parse_args


def main() -> None:
    """
    Initiates an instance of ForecastLoop and optionally prompts the 
        user to run the program in Fahrenheit or Celsius.
    """
    temp_scale = parse_args()

    if temp_scale is None:
        print_wrapped(ENTER_TEMP_SCALE_PROMPT)

    while True:
        try:
            if temp_scale is None:
                temp_scale = get_temp_scale()
            forecast_loop = ForecastLoop()
            if temp_scale in CELSIUS_INPUTS:
                forecast_loop.celsius()
            elif temp_scale in FAHRENHEIT_INPUTS:
                forecast_loop.fahrenheit()
        except KeyboardInterrupt:
            print_padding()
            program_exit()
