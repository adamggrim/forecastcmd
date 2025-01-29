import re


class ParsingRegexes:
    """
    Compiled regular expressions and string for parsing forecast data.

    Attributes:
        AM_PM_BOUNDARY: Compiled regular expression object that 
            captures the boundary between a time value and a.m. or p.m.
        AM_PM_FORMAT: Compiled regular expression object that captures 
            a.m. and p.m. strings for reformatting.
        DUPLICATE_SPACES: Compiled regular expression object that 
            captures duplicate spaces and trailing whitespace.
    """
    AM_PM_BOUNDARY: re.Pattern[str] = re.compile(r'(?<=\d)(?=am|pm)')
    AM_PM_FORMAT: re.Pattern[str] = re.compile(r'(?<=\d\s(a|p))m\.?')
    DUPLICATE_SPACES: re.Pattern[str] = re.compile(r'(?<=\s)\s|\s+$')


class ValidationRegexes:
    """
    Compiled regular expressions for validating input data.

    Attributes:
        URL: Compiled regular expression object that captures any 
            string that matches weather.gov's forecast URL syntax.
        ZIP_CODE: Compiled regular expression object that captures any 
            string that is only a sequence of five digits.
    """
    URL: re.Pattern[str] = re.compile(
        r'^https?://forecast\.weather\.gov/MapClick\.php\?lat=(-?\d+\.\d+)&lon'
        r'=(-?\d+\.\d+)(&FcstType=text&unit=1)?$'
    )
    ZIP_CODE: re.Pattern[str] = re.compile(r'^\d{5}$')
