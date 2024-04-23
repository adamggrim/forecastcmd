import argparse
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

from forecastcmd.regexes import ParsingRegexes
from forecastcmd.validation import HTMLElementNotFoundError


def parse_args() -> Optional[str]:
    """
    Parses command-line arguments for a temperature scale specification.

    Returns:
        temp_scale (Optional[str]): A string representing a specified temperature 
            scale, otherwise None.
    """
    parser = argparse.ArgumentParser(description='Make an optional '
                                     'specification for a temperature scale.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--celsius', action='store_true', help='get the '
                        'forecast in Celsius')
    group.add_argument('-f', '--fahrenheit', action='store_true', 
                        help='get the forecast in Fahrenheit')
    args = parser.parse_args()
    if args.celsius:
        temp_scale = 'celsius'
    elif args.fahrenheit:
        temp_scale = 'fahrenheit'
    else:
        temp_scale = None
    return temp_scale


def f2c(fahrenheit_temps: list[str]) -> list[str]:
    """
    Converts a list of Fahrenheit temperature strings to Celsius.

    Args:
        fahrenheit_temps (list[str]): A list of Fahrenheit temmperature 
            strings.
    
    Returns:
        celsius_temps (list[str]): A list of Celsius temperature 
            strings.
    """
    celsius_temps = [str(round((int(temp) - 32) * 5 / 9)) 
                    for temp in fahrenheit_temps]
    return(celsius_temps)


def parse_forecast(url: str) -> list[str]:
    """
    Extracts the forecast from the HTML for a given URL.

    Args:
        url (str): The url to access for weather data.

    Returns:
        day_forecasts (list[str]): A list of strings pairing each day 
            string with a forecast string.
    """
    nws_page = requests.get(url)
    soup = BeautifulSoup(nws_page.content, 'html.parser')
    forecast_body = soup.find('div', {'id': 'detailed-forecast-body'})
    if forecast_body is None:
        raise HTMLElementNotFoundError('Forecast body not found for that zip '
                                       'code.')
    days = [b.string for b in forecast_body.find_all('b')]
    if days is None:
        raise HTMLElementNotFoundError('Forecast days not found for that zip '
                                       'code.')
    forecasts = [forecast_text.get_text() for forecast_text in 
                    soup.select('div[class *= "forecast-text"]')]
    if not forecasts:
        raise HTMLElementNotFoundError('Forecast text not found for that zip '
                                       'code.')
    # Reverse the order of the strings so the current day appears 
    # closest to the console prompt in the output.
    day_forecasts = [day + ": " + forecast for day, forecast in 
                    zip(days[::-1], forecasts[::-1])]
    return day_forecasts


def format_forecasts(day_forecasts: list[str]) -> list[str]:
    """
    Formats the forecast list elements for printing.

    Args:
        day_forecasts (list[str]): A list of strings representing days 
            and their forecasts, beginning with the most immediate 
            forecast.

    Returns:
        day_forecasts (list[str]): A list of reformatted strings.
    """
    for index, day_forecast in enumerate(day_forecasts):
        # Remove extra spaces.
        day_forecast = ParsingRegexes.spaces_regex.sub('', day_forecast)
        # Add a space before a.m. and p.m.
        day_forecast = ParsingRegexes.am_pm_space_regex.sub(' ', day_forecast)
        # Standardize the format of a.m. and p.m.
        day_forecast = ParsingRegexes.am_pm_format_regex.sub('.m.', 
                                                            day_forecast)
        day_forecasts[index] = day_forecast
    return day_forecasts


def convert_forecasts(day_forecasts: list[str]) -> list[str]:
    """
    Finds forecast temperatures and converts them to Celsius.

    Args:
        day_forecasts (list[str]): A list of strings representing days 
            and their forecasts, beginning with the most immediate 
            forecast.

    Returns:
        formatted_forecasts (list[str]): A list of strings with the  
            temperatures converted to Celsius.
    """
    formatted_forecasts = format_forecasts(day_forecasts)
    for index, day_forecast in enumerate(formatted_forecasts):
        # Find all Fahrenheit temperatures and put them in a list.
        fahrenheit_temps = ParsingRegexes.temps_finder_regex.findall(
            day_forecast)
        # Convert the list of Fahrenheit temperatures to Celsius.
        celsius_temps = f2c(fahrenheit_temps)
        # Loop over Fahrenheit temperatures and substitute with Celsius.
        for temp_index, temp in enumerate(fahrenheit_temps):
            day_forecast = re.sub(rf'-?{temp}\b{ParsingRegexes.lookahead}', 
                                celsius_temps[temp_index], day_forecast)
        formatted_forecasts[index] = day_forecast
    return formatted_forecasts