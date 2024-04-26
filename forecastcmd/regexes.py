import re


class ParsingRegexes:
    """
    Compiled regular expressions for parsing forecast data.
    
    Attributes:
        AM_PM_SPACE (Pattern): Compiled regular expression object that 
            captures the boundary between a time value and a.m. and p.m.
        AM_PM_FORMAT (Pattern): Compiled regular expression object that 
            captures a.m. and p.m. strings for reformatting.
        LOOKAHEAD_STR (str): Regular expression string to ignore 
            numbers in the forecast that are not temperatures.
        SPACES (Pattern): Compiled regular expression object that 
            captures duplicate spaces and trailing whitespace.
        TEMPS_FINDER (Pattern): Compiled regular expression object to 
            capture numbers in a forecast that are temperatures.
    """
    LOOKAHEAD_STR = r'(?!\spercent|%|\sa\.m\.|\sp\.m\.|\sto|\smph|\sand|\sinch)'

    AM_PM_SPACE = re.compile(r'(?<=\d)(?=am|pm)')
    AM_PM_FORMAT = re.compile(r'(?<=\d\s(a|p))m\.?')
    SPACES = re.compile(r'(?<=\s)\s|\s+$')
    TEMPS_FINDER = re.compile(r'-?\d{1,3}\b' + LOOKAHEAD_STR)


class ValidationRegexes:
    """
    Compiled regular expressions for validating input data.

    Attributes:
        url (Pattern): Compiled regular expression object that captures 
            any string that matches weather.gov's forecast URL syntax.
        zip_code (Pattern): Compiled regular expression object that 
            captures any string that is only a sequence of five digits.
    """
    URL = re.compile(r'^https?://forecast\.weather\.gov/MapClick\.php\?'
                        r'lat=(-?\d+\.\d+)&lon=(-?\d+\.\d+)$')
    ZIP_CODE = re.compile(r'^\d{5}$')