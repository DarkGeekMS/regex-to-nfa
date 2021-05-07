import re
import sys
from src.build_nfa import transform
#from src.visualize_nfa import visualize


# global constant regex
RANGES = "\[.-.\]|\[.-..-.\]"
LETTERS = "[A-Za-z]"
DIGITS = "[0-9]"
SPECIALS = "\(|\)|\||\+|\*"


def validate(regex):
    # check whether input expression contains ranges or not
    if re.search(RANGES, regex):
        # exit in case of ranges (ranges not allowed)
        raise Exception("Ranges are NOT allowed !")
    # check validity of each character (escapable special characters)
    idx = 0
    while idx < len(regex):
        # check if the character is not a letter nor a number nor a special
        if not (re.search(LETTERS, regex[idx]) or re.search(DIGITS, regex[idx]) \
            or re.search(SPECIALS, regex[idx])):
            # other special characters must be preceded with '\'
            if regex[idx] == "\\":
                idx += 1
            else:
                raise Exception("Use \ to escape special characters !")
        idx += 1
    # try compiling input expression
    # check for general regex syntax and brackets match
    try:
        re.compile(regex)
    except re.error:
        raise Exception("Input Regex is incorrect !")


def convert(regex):
    # validate input regex
    validate(regex)
    # transform regex to nfa
    nfa = transform(regex)
    # visualize nfa
    #visualize(nfa)


if __name__ == "__main__":
    # initialize regex-to-nfa conversion
    if len(sys.argv) == 2:
        convert(sys.argv[1])
    else:
        raise Exception("Enter Target Regex !")
