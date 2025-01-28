import re


class ParsingRegexes:
    """
    Compiled regular expressions and string for parsing forecast data.
    
    Attributes:
        NOT_TEMPS_LOOKAHEAD: Regular expression lookahead pattern that 
            ignores numbers in the forecast that are not temperatures.

        AM_PM_SPACE: Compiled regular expression object that captures 
            the boundary between a time value and a.m. or p.m.
        AM_PM_FORMAT: Compiled regular expression object that captures 
            a.m. and p.m. strings for reformatting.
        SPACES: Compiled regular expression object that captures 
            duplicate spaces and trailing whitespace.
        TEMPS_FINDER: Compiled regular expression object that captures 
            numbers in a forecast that are temperatures.
        WINDS_FINDER: Regular expression pattern that captures numbers 
            in the forecast that are wind speeds.
    """
    NOT_TEMPS_LOOKAHEAD: str = (
        r'(?!\spercent|%|\sa\.m\.|\sp\.m\.|\sto|\smph|\sand|\sof\san'
        r'|\sinch)'
    )

    AM_PM_SPACE: re.Pattern[str] = re.compile(r'(?<=\d)(?=am|pm)')
    AM_PM_FORMAT: re.Pattern[str] = re.compile(r'(?<=\d\s(a|p))m\.?')
    SPACES: re.Pattern[str] = re.compile(r'(?<=\s)\s|\s+$')
    TEMPS_FINDER: re.Pattern[str] = re.compile(
        r'\b(-?\d{1,3})\b' + NOT_TEMPS_LOOKAHEAD
    )
    WINDS_FINDER: re.Pattern[str] = re.compile(
        r'\b(\d{1,3})(?:\s+to\s+(\d{1,3}))?\smph'
    )


class ValidationRegexes:
    """
    Compiled regular expressions for validating input data.

    Attributes:
        url: Compiled regular expression object that captures any 
            string that matches weather.gov's forecast URL syntax.
        zip_code: Compiled regular expression object that captures any 
            string that is only a sequence of five digits.
    """
    URL: re.Pattern[str] = re.compile(
        r'^https?://forecast\.weather\.gov/MapClick\.php\?lat=(-?\d+\.\d+)&lon'
        r'=(-?\d+\.\d+)$'
    )
    ZIP_CODE: re.Pattern[str] = re.compile(r'^\d{5}$')
