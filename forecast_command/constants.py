class HelpMessages:
    """
    Help message strings for command-line arguments.

    Attributes:
        DESCRIPTION: Description for temperature scale arguments

        CELSIUS: Help message for -c/--celsius argument
        FAHRENHEIT: Help message for -f/--fahrenheit argument
    """
    DESCRIPTION: str = 'Make an optional specification for temperature scale.'

    CELSIUS: str = 'get the forecast in Celsius'
    FAHRENHEIT: str = 'get the forecast in Fahrenheit'

# String printed to prompt the user for another zip code
ANY_OTHER_ZIP_PROMPT: str = 'Any other zip code? (5 digits):'

# Set of strings for selecting Celsius
CELSIUS_INPUTS: set[str] = {'celsius', 'c'}

# String printed to prompt the user to enter a temperature scale
ENTER_TEMP_SCALE_PROMPT: str = (
    'Enter a temperature scale (Celsius [C] or Fahrenheit [F]):'
)

# String printed when the previous temperature scale input was invalid
ENTER_VALID_TEMP_SCALE_PROMPT: str = (
    'Please enter Celsius (C) or Fahrenheit (F):'
)

# String printed when the previous zip code input was invalid
ENTER_VALID_ZIP_PROMPT: str = 'Please enter a valid zip code:'

# String printed to prompt the user to enter a zip code
ENTER_ZIP_PROMPT: str = 'Enter zip code (5 digits):'

# Set of strings for exiting the program
EXIT_INPUTS: set[str] = {'quit', 'q', 'exit', 'e'}

# String printed when the user exits the program
EXIT_MESSAGE: str = 'Exiting the program...'

# Set of strings for selecting Fahrenheit
FAHRENHEIT_INPUTS: str = {'fahrenheit', 'f'}

# Set of strings for indicating a negative response
NO_INPUTS: set[str] = {'no', 'n'}

# Set of strings for indicating an affirmative response
YES_INPUTS: set[str] = {'yes', 'y'}
