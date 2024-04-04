# Forecast Command

`forecastcmd` is a Python package for retrieving weather forecasts from NOAA (National Oceanic and Atmospheric Administration) and printing them to the console. For a given zip code, a seven-day forecast can print in Fahrenheit or Celsius.

## Requirements

- Python 3.6

## Dependencies

`forecastcmd` requires the following Python libraries:

- `beautifulsoup4`: For parsing HTML data retrieved from weather.gov
- `requests`: For making HTTP requests to retrieve forecast data from weather.gov
- `setuptools`: For building and installing the `forecastcmd` package, and for implementing command-line functionality using entry points

You can install these dependencies using pip:

`pip install beautifulsoup4`

`pip install requests`

`pip install setuptools `

## Example

This example demonstrates how to retrieve a weather forecast using `forecastcmd`.

1. **Run the command**

    Once `forecastcmd` is installed, call `forecast` from the command line.

    For a forecast in Celsius, you can also call `forecast -c` from the command line. For a forecast in Fahrenheit, you can call `forecast -f`.

2. **Enter a temperature scale**

    If you did not already indicate a temperature scale, the program will prompt you to enter one:

    ```
    Enter a temperature scale (Celsius [C] or Fahrenheit [F]):
    Celsius
    ```

3. **Enter a zip code**

    The program will prompt you to enter a zip code:
    
    ```
    Enter zip code (5 digits):
    80204
    ```

4. **Print the forecast**

    The program will print a seven-day weather forecast in reverse chronological order, so that the current day appears closest to the console prompt in the output:

    ```
    Sunday: A chance of rain. Partly sunny, with a high near 12.

    Saturday Night: A chance of rain. Mostly cloudy, with a low around 6.

    Saturday: Mostly sunny, with a high near 20.

    Friday Night: Partly cloudy, with a low around 1.

    Friday: A chance of rain before noon. Partly sunny, with a high near 15.

    Thursday Night: A chance of snow. Mostly cloudy, with a low around 2.

    Thursday: A chance of snow. Partly cloudy, with a high near 13.

    Wednesday Night: Mostly cloudy, with a low around 10.

    Wednesday: Mostly sunny, with a high near 22.

    Tuesday Night: Mostly cloudy, with a low around 5.

    Tuesday: Sunny, with a high near 18.

    Monday Night: Mostly clear, with a low around 1.

    Monday: Sunny, with a high near 20.

    Overnight: Mostly clear, with a low around 3.
    ```

5. **Continue or exit**

    The program will ask if you want to enter another zip code. To exit, type 'no' ('n'), 'quit' ('q') or 'exit' ('e'), or trigger a KeyboardInterrupt (Ctrl + C).

    ```
    Any other zip code?:
    ^C

    Exiting the program...
    ```

## Structure

```
├── forecastcmd/
│   ├── __init__.py: File for recognizing forecastcmd as a package
│   ├── __main__.py: File for running the forecast command
│   ├── config.py: Opens the JSON file for use in the program
│   ├── constants.py: Defines constants used throughout the program
│   ├── enums.py: Defines the enum for selecting the temperature scale
│   ├── input_output.py: Handles user input and console output
│   ├── parsing.py: Parses input and HTML data from weather.gov
│   ├── regexes.py: Defines regular expressions for parsing
│   └── validation.py: Functions for zip code and URL validation
└── data/
    └── zip_codes_forecast_urls_dict.json: Maps zip code strings to weather.gov forecast URL strings
```

## Usage

Follow these steps to run `forecastcmd`:

1. **Review dependencies**: Make sure the required Python libraries are installed: `beautifulsoup4`, `requests` and `setuptools`.
2. **Install the package**: Install `forecastcmd` by running `pip install git+https://github.com/adamggrim/forecastcmd.git`.
3. **Run the program**: Execute the program by calling `forecast`, `forecast -c` (for Celsius) or `forecast -f` (for Fahrenheit) from the command line.

## License

This project is licensed under the MIT License.

## Contributors

- Adam Grim (@adamggrim)