import re


class ParsingRegexes:
    """
    Compiled regular expressions and string for parsing forecast data.

    Attributes:
        _WINDS_RANGE: Regular expression pattern that captures the 
            substring following the first number in a wind speed range.

        _NOT_TEMPS_LOOKAHEAD: Regular expression lookahead pattern that 
            ignores numbers in the forecast that are not temperatures.

        ACCUMULATION_FINDER: Compiled regular expression object that
            captures the number of inches of rain or snow accumulation.
        AM_PM_BOUNDARY: Compiled regular expression object that 
            captures the boundary between a time value and a.m. or p.m.
        AM_PM_FORMAT: Compiled regular expression object that captures 
            a.m. and p.m. strings for reformatting.
        DUPLICATE_SPACES: Compiled regular expression object that 
            captures duplicate spaces and trailing whitespace.
        TEMPS_FINDER: Compiled regular expression object that captures 
            numbers in a forecast that are temperatures.
        WINDS_FINDER: Regular expression pattern that captures numbers 
            in the forecast that are wind speeds.
    """
    _NOT_TEMPS_LOOKAHEAD: str = (
        r'(?!\.\d|\spercent|%|\sa\.m\.|\sp\.m\.|\sto|\smph|\sand|\sof\san'
        r'|\sinch)'
    )

    ACCUMULATION_FINDER: re.Pattern[str] = re.compile(
        r'\b(\d{1,3})(?=\s(inch|and{1,3}\sinch))'
    )
    AM_PM_BOUNDARY: re.Pattern[str] = re.compile(r'(?<=\d)(?=am|pm)')
    AM_PM_FORMAT: re.Pattern[str] = re.compile(r'(?<=\d\s(a|p))m\.?')
    DUPLICATE_SPACES: re.Pattern[str] = re.compile(r'(?<=\s)\s|\s+$')
    INCHES_FINDER: re.Pattern[str] = re.compile(r'\binch(es)?\b')
    MPH_FINDER: re.Pattern[str] = re.compile(r'\bmph\b')
    TEMPS_FINDER: re.Pattern[str] = re.compile(
        r'\b(-?\d{1,3})\b' + _NOT_TEMPS_LOOKAHEAD
    )
    WINDS_FINDER: re.Pattern[str] = re.compile(
        r'\b(\d{1,3})(?=\s(mph|to\s\d{1,3}\smph))'
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
