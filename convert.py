import re
import sys
from src.build_nfa import transform
from src.visualize_nfa import visualize
from src.transitiontable_nfa import table

# global constant regex
RANGE = "\[.-.\]|\[.-..-.\]"
LETTER = "[A-Za-z]"
DIGIT = "[0-9]"
SPECIAL = "\(|\)|\||\+|\*"

def validate(regex):
    # check whether input expression contains RANGEZ or not
    if re.search(RANGE, regex):
        # exit in case of RANGE (RANGE not allowed)
        raise Exception("RANGES are NOT allowed !")
    # check validity of each character (escapable special characters)
    idx = 0
    while idx < len(regex):
        # check if the character is not a letter nor a number nor a special
        if not (re.search(LETTER, regex[idx]) or re.search(DIGIT, regex[idx]) \
            or re.search(SPECIAL, regex[idx])):
            # other special characters must be preceded with '\'
            if regex[idx] == "\\":
                idx += 1
            else:
                raise Exception("Use \ to escape special characters !")
        idx += 1

    try:
        re.compile(regex)
    except re.error:
        raise Exception("Input Regex is incorrect !")

# the main function calling all other worker functions
def convert(regex):
    validate(regex)

    nfa = transform(regex)

    visualize(nfa)

    table(nfa)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        convert(sys.argv[1])
    else:
        raise Exception("No regular recieved !")
