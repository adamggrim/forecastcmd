from forecastcmd.input_output import (ForecastLoop, print_wrapped, 
                                      print_padding, program_exit, 
                                      get_temp_scale)
from forecastcmd.constants import (CELSIUS_STRS, ENTER_TEMP_SCALE_STR, 
                                   FAHRENHEIT_STRS)
from forecastcmd.parsing import parse_args


def main() -> None:
    """
    Initiates an instance of ForecastLoop and optionally prompts the 
        user to run the program in Fahrenheit or Celsius.
    """
    temp_scale = parse_args()

    if temp_scale is None:
        print_wrapped(ENTER_TEMP_SCALE_STR)

    while True:
        try:
            if temp_scale is None:
                temp_scale = get_temp_scale()
            forecast_loop = ForecastLoop()
            if temp_scale in CELSIUS_STRS:
                forecast_loop.celsius()
            elif temp_scale in FAHRENHEIT_STRS:
                forecast_loop.fahrenheit()
        except KeyboardInterrupt:
            print_padding()
            program_exit()
