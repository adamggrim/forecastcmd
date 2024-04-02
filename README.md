# Forecast Command

`forecastcmd` is a Python package for retrieving weather forecasts from NOAA (National Oceanic and Atmospheric Administration) and printing them to the console. For a given zip code, a seven-day forecast can print in Fahrenheit or Celsius.

## Requirements

- Python 3.6

## Dependencies

`forecastcmd` requires the following Python libraries:

- `beautifulsoup4`: For parsing HTML data retrieved from weather.gov
- `requests`: For making HTTP requests to retrieve forecast data from weather.gov
- `setuptools`: For implementing command line functionality

You can install these dependencies using pip:

`pip install requests`
`pip install beautifulsoup4`

## Example

This example demonstrates how to retrieve a weather forecast.

1. **Run the command:**

    Once installed, run `forecast` from the command line.

    For a forecast in Fahrenheit, you can also run `forecast -f` from the command line. For a forecast in Celsius, you can run `forecast -c`.

2. **Enter a temperature scale**

    If you did not already indicate a temperature scale, the program will prompt you to enter one.

    ```
    Enter a temperature scale (Fahrenheit [F] or Celsius [C]):
    ```

3. **Enter zip code:**

    The program will prompt you to enter a zip code.
    
    ```
    Enter zip code (5 digits):
    ```

4. **See the forecast:**

    The program will print a weather forecast for the entered zip code.

5. **Continue or exit:**
    The program will ask if you want to enter another zip code. To exit, type 'no' ('n'), 'quit' ('q') or 'exit' ('e'), or trigger a KeyboardInterrupt (Ctrl + C).

    ```
    Any other zip code?:
    No

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

1. **Clone the repository**: Clone the repository or download the source code.
2. **Install dependencies**: Install the necessary Python libraries: `beautifulsoup4`, `requests` and `setuptools`.
3. **Run the program**: Execute the program by calling `forecast`, `forecast -c` or `forecast -f` from the command line.

## License

This project is licensed under the MIT License.

## Contributors

- Adam Grim (@adamggrim)