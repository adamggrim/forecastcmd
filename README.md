# Forecast Command

`forecastcmd` is a Python package for retrieving weather forecasts from NOAA (National Oceanic and Atmospheric Administration) and printing them to the console. For a given zip code, a seven-day forecast can print in Fahrenheit or Celsius.

## Requirements

- Python 3.6

## Dependencies

`forecastcmd` requires the following Python libraries:

- `beautifulsoup4`: For parsing HTML data retrieved from weather.gov
- `requests`: For making HTTP requests to retrieve forecast data from weather.gov
- `setuptools`: For building and installing the `forecastcmd` package, and for implementing command-line functionality using entry points

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

    The program will print a seven-day weather forecast in reverse chronological order, so that the current day appears closest to the bottom of the output:

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

    The program will prompt you to enter another zip code. To exit, type `no` (`n`), `quit` (`q`) or `exit` (`e`), or trigger a KeyboardInterrupt (Ctrl + C):

    ```
    Any other zip code?:
    ^C

    Exiting the program...
    ```

## Structure

```
forecastcmd/
└── data/
|   └── zip_codes_forecast_urls_dict.json: Maps zip code strings to weather.gov forecast URL strings
├── __init__.py: File for recognizing forecastcmd as a package
├── __main__.py: File for running the forecast command
├── config.py: Opens the JSON file for use in the package
├── constants.py: Defines constants used throughout the package
├── enums.py: Defines enum for temperature scales
├── input_output.py: Handles user input and console output
├── parsing.py: Parses input, HTML data and command-line arguments
├── regexes.py: Defines regular expressions for parsing
└── validation.py: Defines functions for zip code and URL validation
```

## Usage

Follow these steps to run `forecastcmd`:

1. **Install Python**: Verify that you have Python 3.6 or later. You can install Python at `https://www.python.org/downloads/`.
2. **Review dependencies**: Make sure the required Python packages are installed: `beautifulsoup4`, `requests` and `setuptools`.

    You can check whether these packages are installed using pip's `show` command on each package.

    On macOS:
    ```
    pip3 show beautifulsoup4
    ```

    If the package is not installed, you will receive the warning, `WARNING: Package(s) not found`. You can install a missing package using pip.

    On macOS:
    ```
    pip3 install beautifulsoup4
    ```

3. **Install the package**: Install `forecastcmd` using pip.

    On macOS:

    ```
    pip3 install git+https://github.com/adamggrim/forecastcmd.git
    ```

4. **Run the program**: Execute the program by calling `forecast`, `forecast -c` (for Celsius) or `forecast -f` (for Fahrenheit) from the command line.

## Troubleshooting

If the console cannot find the `forecast` command when you try to run it from the command line, it was not installed on your system PATH.

To resolve this, follow these steps:

1. Find the installed location of the `forecastcmd` package using pip's `show` command.

    On macOS:
    ```
    pip3 show forecastcmd
    ```

    The location of `forecastcmd` will be listed in the command's output. For example:
    ```
    Location: /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages
    ```

2. Once you have determined the location of `forecastcmd`, find the installed location of the `forecast` command file in your parent Python folder.

    On macOS:
    ```
    find /Library/Frameworks/Python.framework/Versions/3.12/ -name forecast
    ```

3. Create a symbolic link to the underlying `forecast` command file and place it in the local directory on your system PATH.

    On macOS:

    ```
    sudo ln -s /Library/Frameworks/Python.framework/Versions/3.12/bin/forecast /usr/local/bin/
    ```

    To find the system PATH, you can type `echo $PATH` into the console (macOS).

## License

This project is licensed under the MIT License.

## Contributors

- Adam Grim (@adamggrim)