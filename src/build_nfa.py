import collections
import json

def solveBracket(regex, end_state, states):
    # Initialize variables for the bracket expression
    b_start = b_prev = b_char = b_end = end_state + 1
    states[b_end] = {"isFinalState": False}

    index = 0
    # Iterate through the characters in the bracket expression
    while index < len(regex):
        if regex[index] in {'|', '+'}:
            # Handle OR operations within the bracket
            index, prev, start, end = ORing(index + 1, regex, states, b_end)
            # Update states based on the OR operation
            states.update({end + 1: {"isFinalState": False, "ε": b_prev, "ε ": prev},
                           end + 2: {"isFinalState": False}})
            states[end].update({"ε": end + 2})
            states[b_end].update({"ε": end + 2})
            b_char, b_end, b_start, b_prev = end + 1, end + 2, end + 2, end + 1
        elif regex[index] == '(':
            # Handle nested brackets
            j = index + 1
            open_brackets, closed_brackets, sub_regex = 1, 0, ""
            while j < len(regex):
                if regex[j] == '(':
                    open_brackets += 1
                elif regex[j] == ')':
                    closed_brackets += 1
                if open_brackets == closed_brackets:
                    break
                sub_regex += regex[j]
                j += 1
            prev, start, end = solveBracket(sub_regex, b_end, states)
            states[b_end].update({"ε": prev})
            b_end, b_start, b_char = end, end, prev
            index += len(sub_regex) + 2
        elif regex[index] == '\\':
            # Handle escaped characters
            index += 1
            b_end += 1
            states[b_end] = {"isFinalState": False}
            states[b_char].update({regex[index]: b_end})
            b_char, b_start = b_end, b_end
            index += 1
        elif regex[index] == '*':
            # Handle zero or more repetitions
            b_end += 1
            states[b_start].update({" ε ": b_char, "  ε  ": b_end})
            states[b_char].update({"ε            ": b_end})
            states[b_end] = {"isFinalState": False}
            b_start = b_end
            index += 1
        else:
            # Handle regular characters
            b_end += 1
            states[b_start].update({regex[index]: b_end})
            states[b_end] = {"isFinalState": False}
            b_char, b_start = b_start, b_end
            index += 1

    return b_prev, b_start, b_end

def ORing(index, regex, states, end_state):
    # Initialize variables for the OR operation
    ORing_start = ORing_prev = ORing_prev_char = ORing_end = end_state + 1
    states[ORing_end] = {"isFinalState": False}

    while index < len(regex):
        if regex[index] in {'|', '+'}:
            # Return when encountering another OR operation
            return index, ORing_prev, ORing_start, ORing_end
        elif regex[index] == '\\':
            # Handle escaped characters within OR operation
            index += 1
            ORing_end += 1
            states[ORing_start].update({regex[index]: ORing_end})
            states[ORing_end] = {"isFinalState": False}
            ORing_prev_char, ORing_start = ORing_start, ORing_end
            index += 1
        elif regex[index] == '(':
            # Handle nested brackets within OR operation
            j = index + 1
            open_brackets, closed_brackets, sub_regex = 1, 0, ""
            while j < len(regex):
                if regex[j] == '(':
                    open_brackets += 1
                elif regex[j] == ')':
                    closed_brackets += 1
                if open_brackets == closed_brackets:
                    break
                sub_regex += regex[j]
                j += 1
            prev, start, end = solveBracket(sub_regex, ORing_end, states)
            states[ORing_end].update({"ε": prev})
            ORing_end, ORing_start, ORing_prev_char = end, end, prev
            index += len(sub_regex) + 1
        elif regex[index] == '*':
            # Handle zero or more repetitions within OR operation
            ORing_end += 1
            states[ORing_start].update({"   ε   ": ORing_prev_char, "     ε     ": ORing_end})
            states[ORing_prev_char].update({"ε        ": ORing_end})
            states[ORing_end] = {"isFinalState": False}
            ORing_start = ORing_end
        else:
            # Handle regular characters within OR operation
            ORing_end += 1
            states[ORing_start].update({regex[index]: ORing_end})
            states[ORing_end] = {"isFinalState": False}
            ORing_prev_char, ORing_start = ORing_start, ORing_end
        index += 1

    return len(regex), ORing_prev, ORing_start, ORing_end

def transform(regex):
    # Initialize states and variables for the NFA transformation
    states = {0: {"isFinalState": False}}
    start_state = end_state = prev_char = prev_start = 0
    n = len(regex)
    i = 0

    while i < n:
        if regex[i] == '\\':
            # Handle escaped characters
            i += 1
            end_state += 1
            states[start_state].update({regex[i]: end_state})
            states[end_state] = {"isFinalState": False}
            prev_char, start_state = start_state, end_state
            i += 1
        elif regex[i] == '(':
            # Handle nested brackets
            j = i + 1
            open_brackets, closed_brackets, sub_regex = 1, 0, ""
            while j < n:
                if regex[j] == '(':
                    open_brackets += 1
                elif regex[j] == ')':
                    closed_brackets += 1
                if open_brackets == closed_brackets:
                    break
                sub_regex += regex[j]
                j += 1
            prev, start, end = solveBracket(sub_regex, end_state, states)
            states[end_state].update({"ε": prev})
            end_state, start_state, prev_char = end, end, prev
            i = i + len(sub_regex) + 2
        elif regex[i] in {'|', '+'}:
            # Handle OR operations
            i, prev, start, end = ORing(i + 1, regex, states, end_state)
            # Update states based on the OR operation
            states.update({end + 1: {"isFinalState": False, "     ε     ": prev_start, "      ε       ": prev},
                           end + 2: {"isFinalState": False}})
            states[end].update({"ε": end + 2})
            states[end_state].update({"ε": end + 2})
            prev_char, end_state, start_state, prev_start = end + 1, end + 2, end + 2, end + 1
        elif regex[i] == '*':
            # Handle zero or more repetitions
            end_state += 1
            states[start_state].update({"ε     ": prev_char, "ε    ": end_state})
            states[prev_start].update({"ε     ": end_state})
            states[end_state] = {"isFinalState": False}
            start_state = end_state
            i += 1
        else:
            # Handle regular characters
            end_state += 1
            states[start_state].update({regex[i]: end_state})
            states[end_state] = {"isFinalState": False}
            prev_char, start_state = start_state, end_state
            i += 1

    # Set the final state as accepting
    states[end_state]["isFinalState"] = True
    # Order the states for consistent output
    states = collections.OrderedDict(sorted(states.items()))

    # Prepare results for JSON output
    results = {"startingState": f"S{prev_start}"}
    for key, value in states.items():
        entry = {k: f"S{v}" if k != "isFinalState" else v for k, v in value.items()}
        results[f"S{key}"] = entry

    # Write results to a JSON file
    with open('out/nfa.json', 'w', encoding='utf-8') as fp:
        json.dump(results, fp, ensure_ascii=False)
    return results
