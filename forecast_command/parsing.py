import argparse
import re

import requests
from bs4 import BeautifulSoup, Tag

from forecast_command.constants import HelpMessages
from forecast_command.regexes import ParsingRegexes
from forecast_command.validation import HTMLElementNotFoundError


def parse_args() -> str | None:
    """
    Parses command-line arguments for a temperature scale specification.

    Returns:
        str | None: A string representing a specified temperature 
            scale, otherwise None.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=HelpMessages.DESCRIPTION
    )
    group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group()
    )
    group.add_argument(
        '-c', 
        '--celsius', 
        action='store_true', 
        help=HelpMessages.CELSIUS
    )
    group.add_argument(
        '-f', 
        '--fahrenheit', 
        action='store_true', 
        help=HelpMessages.FAHRENHEIT
    )
    args: argparse.Namespace = parser.parse_args()
    if args.celsius:
        return 'celsius'
    elif args.fahrenheit:
        return 'fahrenheit'
    else:
        return None


def convert_number_words(text: str) -> str:
    """
    Converts number words in a string to numeral substrings.

    Args:
        text: A string containing number words.

    Returns:
        str: The input string with number words converted to numeral 
            substrings.
    """
    number_words: dict[str, str] = {
        'zero': '0', 
        'a tenth of an': '0.1', 
        'a half': '0.5', 
        'half of an': '0.5', 
        'a quarter of an': '0.25', 
        'one': '1', 
        'two': '2', 
        'three': '3', 
        'four': '4', 
        'five': '5', 
        'six': '6', 
        'seven': '7', 
        'eight': '8', 
        'nine': '9'
    }
    for number_word, number in number_words.items():
        text = re.sub(rf'\b{number_word}\b', number, text)
    return text


def convert_numerals(text: str) -> str:
    """
    Converts the numerals 0 and 0.5 in a string to number words.

    Args:
        text: A string containing the numbers 1, 0 or 0.5.

    Returns:
        str: The input string with the numbers 1, 0 and 0.5 converted 
            to number words.
    """
    numbers_words: dict[str, str] = {
        '0': 'zero', 
        '0.1': 'a tenth of a', 
        '0.5': 'a half'
    }
    for number, number_word in numbers_words.items():
        text = re.sub(rf'\b{number}\b(?!\.\d)', number_word, text)
    return text


def convert_fahrenheit_temps(forecast_text: str) -> str:
    """
    Converts Fahrenheit temperatures in a forecast string to Celsius.

    Args:
        forecast_text: The forecast string with Fahrenheit temperatures.

    Returns:
        str: The forecast string with Celsius temperatures.
    """
    def _f2c(fahrenheit_temp: str) -> str:
        """
        Converts a Fahrenheit temperature string to Celsius.

        Args:
            fahrenheit_temps: A Fahrenheit temperature string.

        Returns:
            str: A Celsius temperature string.
        """
        celsius_temp: int = round((int(fahrenheit_temp) - 32) * 5 / 9)
        return str(celsius_temp)
    return re.sub(
        ParsingRegexes.TEMPS_FINDER, 
        lambda match: _f2c(match.group(1)), 
        forecast_text
    )


def convert_mph_speeds(forecast_text: str) -> str:
    """
    Converts a wind speed range in a forecast string from miles per 
        hour (mph) to kilometers per hour (km/h).

    Args:
        forecast_text: The forecast string with wind speeds in mph.

    Returns:
        str: The forecast string with wind speed in km/h.
    """
    def _mph_to_kmh(mph_speed: str) -> str:
        """
        Converts a wind speed string in miles per hour (mph) to 
            kilometers per hour (km/h).

        Args:
            mph_speed: A wind speed string in mph.

        Returns:
            str: A wind speed string in km/h.
        """
        kmh_speed: int = round(int(mph_speed) * 1.60934)
        return str(kmh_speed)
    kmh_forecast_text = re.sub(
        ParsingRegexes.WINDS_FINDER, 
        lambda match: _mph_to_kmh(match.group(1)), 
        forecast_text
    )
    return re.sub(ParsingRegexes.MPH_FINDER, 'km/h', kmh_forecast_text)


def convert_inches(forecast_text: str) -> str:
    """
    Converts an accumulation range in a forecast string from inches to 
        centimeters.

    Args:
        forecast_text: The forecast string with accumulation in inches.

    Returns:
        str: The forecast string with accumulation in cm.
    """
    def _inches_to_cm(inches_length: str) -> str:
        """
        Converts a length string in inches to centimeters (cm).

        Args:
            inches_length: An accumulation string in inches.

        Returns:
            str: An accumulation string in cm.
        """
        cm_length: int = round(float(inches_length) * 2.54)
        return str(cm_length)
    cm_forecast_text = re.sub(
        ParsingRegexes.ACCUMULATION_FINDER, 
        lambda match: _inches_to_cm(match.group(1)), 
        forecast_text
    )
    return re.sub(ParsingRegexes.INCHES_FINDER, 'centimeters', cm_forecast_text)


def parse_forecast(url: str) -> list[str]:
    """
    Extracts the forecast from the HTML for a given URL.

    Args:
        url: The url to access for weather data.

    Returns:
        list[str]: A list of strings pairing each day string with a 
            forecast string.
    """
    nws_page: requests.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(nws_page.content, 'html.parser')
    forecast_body: Tag | None = soup.find(
        'div', {'id': 'detailed-forecast-body'}
    )
    if forecast_body is None:
        raise HTMLElementNotFoundError(
            'Forecast body not found for that zip code.'
        )
    days: list[str] = [b.string for b in forecast_body.find_all('b')]
    if not days:
        raise HTMLElementNotFoundError(
            'Forecast days not found for that zip code.'
        )
    forecasts_text: list[str] = [
        forecast_text.get_text() 
        for forecast_text in soup.select('div[class *= "forecast-text"]')
    ]
    if not forecasts_text:
        raise HTMLElementNotFoundError(
            'Forecast text not found for that zip code.'
        )
    # Reverse the order of the strings so the current day appears closest to 
    # the console prompt in the output.
    return [
        day + ": " + forecast_text 
        for day, forecast_text in zip(
            days[::-1], forecasts_text[::-1]
        )
    ]


def format_forecasts(forecasts_text: list[str]) -> list[str]:
    """
    Formats the forecast list elements for printing.

    Args:
        forecasts_text: A list of strings representing days and their 
            forecasts, beginning with the soonest forecast.

    Returns:
        forecasts_text: A list of reformatted strings.
    """
    for index, forecast_text in enumerate(forecasts_text):
        # Remove extra spaces.
        forecast_text: str = ParsingRegexes.DUPLICATE_SPACES.sub(
            '', forecast_text
        )
        # Add a space before a.m. and p.m.
        forecast_text = ParsingRegexes.AM_PM_BOUNDARY.sub(' ', forecast_text)
        # Standardize the format of a.m. and p.m.
        forecast_text = ParsingRegexes.AM_PM_FORMAT.sub('.m.', forecast_text)
        forecasts_text[index] = forecast_text
    return forecasts_text


def convert_forecasts(forecasts_text: list[str]) -> list[str]:
    """
    Finds forecast temperatures, wind speeds and accumulation totals 
        and converts them to Celsius, kilometers per hour (km/h) and 
        centimeters (cm).

    Args:
        forecasts_text: A list of strings representing days and their 
            forecasts, beginning with the soonest forecast.

    Returns:
        formatted_forecasts: A list of strings with the temperatures 
            converted to Celsius, wind speeds converted to km/h and 
            accumulation totals converted to cm.
    """
    formatted_forecasts: list[str] = format_forecasts(forecasts_text)
    for index, formatted_forecast in enumerate(formatted_forecasts):
        numerals_forecast: str = convert_number_words(formatted_forecast)
        celsius_forecast: str = convert_fahrenheit_temps(numerals_forecast)
        kmh_forecast: str = convert_mph_speeds(celsius_forecast)
        cm_forecast: str = convert_inches(kmh_forecast)
        number_words_forecast: str = convert_numerals(cm_forecast)
        formatted_forecasts[index] = number_words_forecast
    return formatted_forecasts
