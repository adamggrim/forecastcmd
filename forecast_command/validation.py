from forecast_command.config import zip_codes_dict
from forecast_command.constants import (
    CELSIUS_INPUTS, 
    FAHRENHEIT_INPUTS)
from forecast_command.regexes import ValidationRegexes


class HTMLElementNotFoundError(Exception):
    """Exception raised raised when a given HTML element cannot be 
        found."""


class InvalidTempScaleError(Exception):
    """Exception raised when the provided temperature scale string is 
        invalid."""


class InvalidUrlFormatError(Exception):
    """Exception raised when the provided string does not match 
        weather.gov's forecast URL syntax."""


class InvalidZipCodeFormatError(Exception):
    """Exception raised when the provided string is not a valid zip 
        code."""


class NoTempScaleError(Exception):
    """Exception raised when the provided temperature scale string is 
        empty."""


class NoDataForZipCodeError(Exception):
    """Exception raised when there is no data available for the given 
        zip code."""


class NoZipCodeError(Exception):
    """Exception raised when the provided string is empty."""


class ZipCodeNotFoundError(Exception):
    """Exception raised when the zip code string is not found in the 
        given JSON file."""


def validate_temp_scale(temp_scale_input: str) -> None:
    """
    Validates the temperature scale string by checking whether the 
        string is in the sets CELSIUS_INPUTS or FAHRENHEIT_INPUTS.

    Args:
        temp_scale: A string representing a temperature scale.
    """
    if temp_scale_input == '':
        raise NoTempScaleError('No temperature scale entered.')
    elif (temp_scale_input not in CELSIUS_INPUTS and temp_scale_input not in 
          FAHRENHEIT_INPUTS):
        raise InvalidTempScaleError('Not a valid temperature scale.')


def validate_zip_code(zip_code_input: str) -> None:
    """
    Validates the zip code string passed into the function by checking 
        whether the string is only a sequence of five digits.

    Args:
        zip_code_input: A string representing a zip code.
    """
    if zip_code_input == '':
        raise NoZipCodeError('No zip code entered.')
    elif not ValidationRegexes.ZIP_CODE.match(zip_code_input):
        raise InvalidZipCodeFormatError('Invalid zip code format.')
    elif zip_code_input not in zip_codes_dict:
        raise ZipCodeNotFoundError('Zip code not found.')
    elif zip_codes_dict[zip_code_input] == '':
        raise NoDataForZipCodeError(f'No data available for {zip_code_input}.')


def validate_url(url: str) -> None:
    """
    Validates the URL string passed into the function by checking 
        whether the string matches weather.gov's forecast URL syntax.

    Args:
        url: A string representing a URL.
    """
    if not ValidationRegexes.URL.match(url):
        raise InvalidUrlFormatError('Invalid URL for that zip code.')
