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


def f2c(fahrenheit_temps: list[str]) -> list[str]:
    """
    Converts a list of Fahrenheit temperature strings to Celsius.

    Args:
        fahrenheit_temps: A list of Fahrenheit temperature 
            strings.

    Returns:
        list[str]: A list of Celsius temperature strings.
    """
    return [str(round((int(temp) - 32) * 5 / 9)) for temp in fahrenheit_temps]


def mph_to_kmh(mph_speeds: list[str]) -> list[str]:
    """
    Converts a list of miles per hour (mph) wind speed strings to 
        kilometers per hour (km/h).

    Args:
        mph_speeds: A list of wind speed strings in mph.

    Returns:
        list[str]: A list of wind speed strings in km/h.
    """
    return [str(round(float(speed) * 1.60934)) for speed in mph_speeds]


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
    forecasts: list[str] = [
        forecast_text.get_text() 
        for forecast_text in soup.select('div[class *= "forecast-text"]')
    ]
    if not forecasts:
        raise HTMLElementNotFoundError(
            'Forecast text not found for that zip code.'
        )
    # Reverse the order of the strings so the current day appears closest to 
    # the console prompt in the output.
    return [
        day + ": " + forecast 
        for day, forecast in zip(
            days[::-1], forecasts[::-1]
        )
    ]


def format_forecasts(day_forecasts: list[str]) -> list[str]:
    """
    Formats the forecast list elements for printing.

    Args:
        day_forecasts: A list of strings representing days and their 
            forecasts, beginning with the most immediate forecast.

    Returns:
        day_forecasts: A list of reformatted strings.
    """
    for index, day_forecast in enumerate(day_forecasts):
        # Remove extra spaces.
        day_forecast: str = ParsingRegexes.SPACES.sub('', day_forecast)
        # Add a space before a.m. and p.m.
        day_forecast = ParsingRegexes.AM_PM_SPACE.sub(' ', day_forecast)
        # Standardize the format of a.m. and p.m.
        day_forecast = ParsingRegexes.AM_PM_FORMAT.sub('.m.', day_forecast)
        day_forecasts[index] = day_forecast
    return day_forecasts


def convert_forecasts(day_forecasts: list[str]) -> list[str]:
    """
    Finds forecast temperatures and converts them to Celsius.

    Args:
        day_forecasts: A list of strings representing days and their 
            forecasts, beginning with the most immediate forecast.

    Returns:
        formatted_forecasts: A list of strings with the temperatures 
            converted to Celsius.
    """
    formatted_forecasts: list[str] = format_forecasts(day_forecasts)
    for index, day_forecast in enumerate(formatted_forecasts):
        # Find all Fahrenheit temperatures and put them in a list.
        fahrenheit_temps: list[str] = (
            ParsingRegexes.TEMPS_FINDER.findall(day_forecast)
        )
        # Convert the list of Fahrenheit temperatures to Celsius.
        celsius_temps: list[str] = f2c(fahrenheit_temps)
        # Loop over Fahrenheit temperatures and substitute with Celsius.
        for temp_index, temp in enumerate(fahrenheit_temps):
            day_forecast: str = re.sub(
                rf'-?{temp}\b{ParsingRegexes.NOT_TEMPS_LOOKAHEAD}', 
                celsius_temps[temp_index], day_forecast
            )
        formatted_forecasts[index] = day_forecast
    return formatted_forecasts
