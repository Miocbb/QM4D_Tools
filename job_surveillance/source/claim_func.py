"""
supporting functions
"""
import sys


def SigExit(*string):
    for i in string:
        print i,
    sys.exit()


def string_combine(*string):
    """
    combine string with whitespace as delimeter

    Input: <type: str> str1, str2, ...
    Output: <type: str> combiened_str
    """
    combined_str = ''
    for i in string:
        combined_str += i + ' '
    return combined_str.rstrip()
