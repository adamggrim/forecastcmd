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


def number_words_to_numerals(text: str) -> str:
    """
    Converts number words in a string to number substrings.

    Args:
        text: A string containing number words.

    Returns:
        str: The input string with number words converted to number 
            substrings.
    """
    number_words: dict[str, str] = {
        'a half': '0.5', 
        'zero': '0', 
        'one': '1', 
        'two': '2', 
        'three': '3', 
        'four': '4', 
        'five': '5', 
        'six': '6', 
        'seven': '7', 
        'eight': '8', 
        'nine': '9', 
    }
    for number_word, number in number_words.items():
        text = re.sub(rf'\b{number_word}\b', number, text)
    return text


def numerals_to_number_words(text: str) -> str:
    """
    Converts the numbers 0 and 0.5 in a string to number words.

    Args:
        text: A string containing the numbers 1, 0 or 0.5.

    Returns:
        str: The input string with the numbers 1, 0 and 0.5 converted 
            to number words.
    """
    numbers_words: dict[str, str] = {
        '0.5': 'a half', 
        '0': 'zero', 
    }
    for number, number_word in numbers_words.items():
        text = re.sub(rf'\b{number}\b', number_word, text)
    return text


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


def mph_to_kmh_range(mph_range: str) -> str:
    """
    Converts a wind speed range string in miles per hour (mph) to 
        kilometers per hour (km/h).

    Args:
        mph_speed: A wind speed range string in mph.

    Returns:
        str: A wind speed range string in km/h.
    """
    def mph_to_kmh(mph_speed: str) -> str:
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
    winds_match: re.Match[str] | None = re.search(
        ParsingRegexes.WINDS_FINDER, mph_range
    )
    if winds_match:
        lower_mph: str = winds_match.group(1)
        lower_kmh: str = mph_to_kmh(lower_mph)

        if winds_match.group(2):
            upper_mph: str = winds_match.group(2)
            upper_kmh: str = mph_to_kmh(upper_mph)
            return mph_range.replace(
                winds_match.group(0), f'{lower_kmh} to {upper_kmh} km/h'
            )

        return mph_range.replace(
            winds_match.group(0), f'{lower_kmh} km/h'
        )

    return mph_range


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
            forecasts, beginning with the soonest forecast.

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
    Finds forecast temperatures and wind speeds and converts them to 
        Celsius and kilometers per hour (km/h).

    Args:
        day_forecasts: A list of strings representing days and their 
            forecasts, beginning with the soonest forecast.

    Returns:
        formatted_forecasts: A list of strings with the temperatures 
            converted to Celsius and wind speeds converted to km/h.
    """
    formatted_forecasts: list[str] = format_forecasts(day_forecasts)
    for index, day_forecast in enumerate(formatted_forecasts):
        numerals_day_forecast = number_words_to_numerals(day_forecast)
        # Find all Fahrenheit temperatures and put them in a list.
        fahrenheit_temps: list[str] = (
            ParsingRegexes.TEMPS_FINDER.findall(numerals_day_forecast)
        )
        # Convert the list of Fahrenheit temperatures to Celsius.
        celsius_temps: list[str] = f2c(fahrenheit_temps)
        # Loop over Fahrenheit temperatures and substitute with Celsius.
        for temp_index, temp in enumerate(fahrenheit_temps):
            numerals_day_forecast: str = re.sub(
                rf'-?{temp}\b{ParsingRegexes.NOT_TEMPS_LOOKAHEAD}', 
                celsius_temps[temp_index], numerals_day_forecast
            )
        # Find all mph wind speeds and put them in a list.
        mph_winds: list[str] = (
            ParsingRegexes.WIND_FINDER.findall(day_forecast)
        )
        kmh_winds: list[str] = mph_to_kmh(mph_winds)
        for wind_index, mph_wind in enumerate(mph_winds):
            day_forecast: str = re.sub(
                rf'{mph_wind}{ParsingRegexes.WIND_LOOKAHEAD}', 
                kmh_winds[wind_index], day_forecast
            )
        formatted_forecasts[index] = day_forecast
    return formatted_forecasts
