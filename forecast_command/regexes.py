import re
from typing import Pattern


class ParsingRegexes:
    """
    Compiled regular expressions and string for parsing forecast data.
    
    Attributes:
        AM_PM_SPACE (Pattern): Compiled regular expression object that 
            captures the boundary between a time value and a.m. or p.m.
        AM_PM_FORMAT (Pattern): Compiled regular expression object that 
            captures a.m. and p.m. strings for reformatting.
        NOT_TEMPS_LOOKAHEAD (str): Regular expression lookahead pattern that 
            ignores numbers in the forecast that are not temperatures.
        SPACES (Pattern): Compiled regular expression object that 
            captures duplicate spaces and trailing whitespace.
        TEMPS_FINDER (Pattern): Compiled regular expression object that 
            captures numbers in a forecast that are temperatures.
    """
    NOT_TEMPS_LOOKAHEAD: str = (
        r'(?!\spercent|%|\.|\sa\.m\.|\sp\.m\.|\sto|\smph|\sand|\sof\san'
        r'|\sinch)'
    )
    AM_PM_SPACE: Pattern = re.compile(r'(?<=\d)(?=am|pm)')
    AM_PM_FORMAT: Pattern = re.compile(r'(?<=\d\s(a|p))m\.?')
    SPACES: Pattern = re.compile(r'(?<=\s)\s|\s+$')
    TEMPS_FINDER: Pattern = re.compile(r'-?\d{1,3}\b' + NOT_TEMPS_LOOKAHEAD)


class ValidationRegexes:
    """
    Compiled regular expressions for validating input data.

    Attributes:
        url (Pattern): Compiled regular expression object that captures 
            any string that matches weather.gov's forecast URL syntax.
        zip_code (Pattern): Compiled regular expression object that 
            captures any string that is only a sequence of five digits.
    """
    URL: Pattern = re.compile(
        r'^https?://forecast\.weather\.gov/MapClick\.php\?lat=(-?\d+\.\d+)&lon'
        r'=(-?\d+\.\d+)$'
    )
    ZIP_CODE: Pattern = re.compile(r'^\d{5}$')
