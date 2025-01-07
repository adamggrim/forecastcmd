import os
import textwrap

import requests

from forecastcmd.config import zip_codes_dict
from forecastcmd.constants import (
    ANY_OTHER_ZIP_PROMPT, 
    ENTER_VALID_TEMP_SCALE_PROMPT, 
    ENTER_VALID_ZIP_PROMPT, 
    ENTER_ZIP_PROMPT, 
    EXIT_PROMPT, 
    NO_INPUTS, 
    QUIT_INPUTS, 
    YES_INPUTS
)
from forecastcmd.enums import TempScale
from forecastcmd.parsing import (
    convert_forecasts, 
    format_forecasts, 
    parse_forecast
)
from forecastcmd.validation import (
    HTMLElementNotFoundError, 
    InvalidTempScaleError, 
    InvalidUrlFormatError, 
    InvalidZipCodeFormatError, 
    NoDataForZipCodeError, 
    NoTempScaleError, 
    NoZipCodeError, 
    ZipCodeNotFoundError
)
from forecastcmd.validation import (
    validate_temp_scale, 
    validate_url, 
    validate_zip_code
)


class ForecastLoop:
    """
    Prompts the user for input, validates zip codes, and prints 
        the associated forecasts in Fahrenheit or Celsius.
    """
    def __init__(self):
        """
        Initializes a new InputLoop instance by prompting the user to 
            enter a zip code.

        Args:
            self: The instance of the InputLoop class.
        """
        print_wrapped(ENTER_ZIP_PROMPT)
    
    def _zip_input(self, temp_scale: TempScale) -> None:
        """
        Prompts the user to enter a zip code, prints the forecast for 
            that zip code, and prompts the user to enter any other zip 
            code.
        
        Args:
            temp_scale (TempScale): The temperature scale for the 
                forecast.
        """
        # While loop to deploy functions and get input from the user
        while True:
            url: str = retrieve_url_from_zip()
            print_forecast(url, temp_scale)
            print_wrapped(ANY_OTHER_ZIP_PROMPT)
    
    def fahrenheit(self) -> None:
        """
        Runs the input loop for printing forecasts in Fahrenheit.
        
        Args:
            self: The instance of the InputLoop class.
        """
        self._zip_input(TempScale.FAHRENHEIT)
    
    def celsius(self) -> None:
        """
        Runs the input loop for printing forecasts in Celsius.

        Args:
            self: The instance of the InputLoop class.
        """
        self._zip_input(TempScale.CELSIUS)


def print_padding() -> None:
    """Prints a blank line for padding."""
    print('')


def print_wrapped(string: str) -> None:
    """
    Wraps printing based on the width of the terminal and adds a 
        newline character to the start of the string.

    Args:
        text (str): The string to print.
    """
    terminal_size = os.get_terminal_size()[0]
    print_size = terminal_size - 1
    wrapped_str = textwrap.fill(string, width=print_size)
    print('\n' + wrapped_str)


def program_exit() -> None:
    """
    Prints a message that the program is exiting, then exits the 
        program.
    """
    print_wrapped(EXIT_PROMPT)
    print_padding()
    exit()


def prompt_for_temp_scale() -> str:
    """
    Requests a valid temperature scale.

    Returns:
        temp_scale: A string representing Fahrenheit or Celsius.
    """
    while True:
        temp_scale = input().strip().lower()
        if temp_scale in (NO_INPUTS | QUIT_INPUTS):
            program_exit()
        else:
            try:
                validate_temp_scale(temp_scale)
            except (NoTempScaleError, InvalidTempScaleError) as e:
                print_wrapped(str(e))
                print_wrapped(ENTER_VALID_TEMP_SCALE_PROMPT)
            else:
                return temp_scale


def retrieve_url_from_zip() -> str:
    """
    Requests a valid zip code that matches a zip code in the JSON file 
        and returns the matching URL.
    
    Returns:
        url (str): The url for the inputted zip code.
    """
    while True:
        zip_code = input().strip().lower()
        if zip_code in (NO_INPUTS | QUIT_INPUTS):
            program_exit()
        elif zip_code in YES_INPUTS:
            print_wrapped(ENTER_VALID_ZIP_PROMPT)
        else:
            try:
                validate_zip_code(zip_code)
                url = zip_codes_dict[zip_code]
                validate_url(url)
            except (NoZipCodeError, InvalidZipCodeFormatError) as e:
                print_wrapped(str(e))
                print_wrapped(ENTER_VALID_ZIP_PROMPT)
            except (ZipCodeNotFoundError, NoDataForZipCodeError, 
                    InvalidUrlFormatError) as e:
                print_wrapped(str(e))
                print_wrapped()
            else:
                return url


def print_forecast(url: str, temp_scale: TempScale) -> None:
    """
    Prints forecast data from a given URL to the console.

    Args:
        url (str): The URL for accessing weather data.
        temp_scale (TempScale): The temperature scale to apply to the 
            forecast.
    """
    try:
        day_forecasts = parse_forecast(url)
        if temp_scale == TempScale.CELSIUS:
            formatted_forecasts = convert_forecasts(day_forecasts)
        else:
            formatted_forecasts = format_forecasts(day_forecasts)
        for day_forecast in formatted_forecasts:
            print_wrapped(day_forecast)
    except requests.exceptions.ConnectionError:
        print_wrapped('No internet connection. Please try again.')
    except requests.exceptions.Timeout:
        print_wrapped('The request timed out. Please try again.')
    except HTMLElementNotFoundError as e:
        print_wrapped(f'HTML element not found: {e}')
    except Exception as e:
        print_wrapped(f'An unexpected error occurred: {e}')
