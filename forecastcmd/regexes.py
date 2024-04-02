import re


class ParsingRegexes:
    """
    Compiled regular expressions for parsing forecast data.
    
    Attributes:
        spaces_regex (Pattern): Compiled regular expression object that 
            captures duplicate spaces and trailing whitespace.
        am_pm_space_regex (Pattern): Compiled regular expression object 
            that captures the boundary between a time value and a.m. 
            and p.m.
        am_pm_format_regex (Pattern): Compiled regular expression 
            object that captures a.m. and p.m. strings for reformatting.
        lookahead (str): Regular expression string to ignore numbers in 
            the forecast that are not temperatures.
        temps_finder_regex (Pattern): Compiled regular expression 
            object to capture numbers in a forecast that are 
            temperatures.
    """
    spaces_regex = re.compile(r'(?<=\s)\s|\s+$')
    am_pm_space_regex = re.compile(r'(?<=\d)(?=am|pm)')
    am_pm_format_regex = re.compile(r'(?<=\d\s(a|p))m\.?')
    lookahead = r'(?!\spercent|%|\sa\.m\.|\sp\.m\.|\sto|\smph|\sand|\sinch)'
    temps_finder_regex = re.compile(r'-?\d{1,3}\b' + lookahead)


class ValidationRegexes:
    """
    Compiled regular expressions for validating input data.

    Attributes:
        zip_code_regex (Pattern): Compiled regular expression object 
            that captures any string that is only a sequence of five 
            digits.
        url_regex (Pattern): Compiled regular expression object that 
            captures any string that matches weather.gov's forecast URL 
            syntax.
    """
    zip_code_regex = re.compile(r'^\d{5}$')
    url_regex = re.compile(r'^https?://forecast\.weather\.gov/MapClick\.php\?'
                        r'lat=(-?\d+\.\d+)&lon=(-?\d+\.\d+)$')