# operations will be as following : and : 0 , or: 1 
import collections

def solveBracket(regex, end_state, states):
    b_start = end_state + 1
    b_prev = end_state + 1
    b_char = end_state + 1
    b_end = end_state + 1
    states.update( { b_end : { "isTerminatingState": False } })
    index = 0
    while(index < len(regex)):
        if regex[index] == '|':
            index, prev, start,end = oring(index+1, regex, states , b_end)
            states.update( { end+1 : { "isTerminatingState": False, "ε" : b_prev , "ε " : prev } })
            states.update( { end+2 : { "isTerminatingState": False} })
            states[end].update({"ε" : end+2})
            states[b_end].update({"ε" : end+2})
            #updates
            b_char = end + 1
            b_end = end +2
            b_start = b_end
            b_prev = end + 1
            #return (index), oring_prev, oring_start, oring_end
        elif regex[index] == '(':
            open_brackets = 1
            closed_brackets = 0
            sub_regex = ""
            j = index+1
            while(j<len(regex)):
                if regex[j] == '(':
                    open_brackets +=1
                elif regex[j] == ')':
                    closed_brackets +=1
                if (open_brackets == closed_brackets):
                    break
                sub_regex += regex[j]
                j += 1
            prev , start, end = solveBracket(sub_regex, b_end, states) 
            states[b_end].update({"ε" : prev})
            b_end = end
            b_start = b_end
            b_char = prev

            index = index + len(sub_regex) + 1
        elif regex[index] == '\\':
            index += 1
            states[b_end].update({regex[index] : (b_end+1)})
            b_end +=1
            states.update( { b_end : { "isTerminatingState": False } })
            b_char = b_start
            b_start = b_end
        elif regex[index] == '*':
            b_end += 1
            states[b_start].update({"ε          " : b_char, "ε           " : b_end })
            states[b_char].update({"ε            " : b_end})
            states.update( { b_end : { "isTerminatingState": False} })
            b_start = b_end
        else:
            b_end +=1
            states[b_start].update( { regex[index] : b_end })
            states.update( { b_end : { "isTerminatingState": False } })
            b_char = b_start
            b_start = b_end         
        index += 1               
    return b_prev, b_start, b_end

def oring(index , regex, states , end_state):
    oring_start = end_state + 1
    oring_prev = end_state + 1
    oring_prev_char = end_state + 1
    oring_end = end_state + 1
    states.update( { oring_end : { "isTerminatingState": False } })

    while(index < len(regex)):
        if regex[index] == '|':
            return (index), oring_prev, oring_start, oring_end
        if regex[index] == '\\':
            index += 1
            states[oring_end].update({regex[index] : (oring_end+1)})
            oring_end +=1
            states.update( { oring_end : { "isTerminatingState": False } })
            oring_prev_char = oring_start
            oring_start = oring_end

        if regex[index] == '(':
            open_brackets = 1
            closed_brackets = 0
            sub_regex = ""
            j = index+1
            while(j<len(regex)):
                if regex[j] == '(':
                    open_brackets +=1
                elif regex[j] == ')':
                    closed_brackets +=1
                if (open_brackets == closed_brackets):
                    break
                sub_regex += regex[j]
                j += 1
            prev , start, end = solveBracket(sub_regex, oring_end, states) 
            states[oring_end].update({"ε" : prev})
            oring_end = end
            oring_start = oring_end
            oring_prev_char = prev
            index = index + len(sub_regex) + 1

        elif regex[index] == '*':
            oring_end += 1
            states[oring_start].update({"ε      " : oring_prev_char, "ε       " : oring_end })
            states[oring_prev_char].update({"ε        " : oring_end})
            states.update( { oring_end : { "isTerminatingState": False} })
            oring_start = oring_end
        else:
            oring_end +=1
            states[oring_start].update( { regex[index] : oring_end })
            states.update( { oring_end : { "isTerminatingState": False } })
            oring_prev_char = oring_start
            oring_start = oring_end         
        index += 1               
    return len(regex), oring_prev, oring_start, oring_end

def transform(regex):
    states = { 0 : { "isTerminatingState": False } }
    #the state and end state to any expression in the regex
    start_state = 0
    end_state   = 0
    prev_char = 0
    prev_start  = 0
    n = len(regex)
    i = 0
    while i < n:
        # get the last state and add a new transition to it using the char regex[++i]
        # add new state with that character to states dictionary
        if regex[i] == '\\' :
            i += 1
            end_state += 1
            states[start_state].update({regex[i] : end_state})
            states.update( { end_state : { "isTerminatingState": False } })
            prev_char = start_state
            start_state = end_state
            i +=1
            operation = 0
        # in case of open bracket solve the bracket in another function and update i and states in that function 
        elif regex[i] == '(':
            open_brackets = 1
            closed_brackets = 0
            sub_regex = ""
            j = i+1
            while(j<n):
                if regex[j] == '(':
                    open_brackets +=1
                elif regex[j] == ')':
                    closed_brackets +=1
                if (open_brackets == closed_brackets):
                    break
                sub_regex += regex[j]
                j += 1
            prev , start, end = solveBracket(sub_regex, end_state, states) 
            states[end_state].update({"ε" : prev})
            end_state = end
            start_state = end_state
            prev_char = prev
            i = i + len(sub_regex) + 2
        # in case of oring 
        elif regex[i] == '|':
            i, prev, start,end = oring(i+1, regex, states , end_state)
            states.update( { end+1 : { "isTerminatingState": False, "ε" : prev_start , "ε " : prev } })
            states.update( { end+2 : { "isTerminatingState": False} })
            states[end].update({"ε" : end+2})
            states[end_state].update({"ε" : end+2})
            #updates
            prev_char = end + 1
            end_state = end +2
            start_state = end_state
            prev_start = end + 1
        # in case of repetition
        elif regex[i] == '*':
            end_state += 1
            states[start_state].update({"ε   " : prev_char, "ε    " : end_state })
            states[prev_char].update({"ε     " : end_state})
            states.update( { end_state : { "isTerminatingState": False} })
            start_state = end_state
            i += 1
        # general case ( anding )
        else:
            end_state += 1
            states[start_state].update({regex[i] : end_state})
            states.update( { end_state : { "isTerminatingState": False } })
            prev_char = start_state
            start_state = end_state
            i += 1

    states[end_state]["isTerminatingState"] = True
    states = collections.OrderedDict(sorted(states.items()))
    for k, v in states.items(): print(k, v)
    # loop over states and save them with the given example to json file
    # return that json file
    return None


"""
Assume i have input like that : "(A|B)C"
so we need to loop over each string : 
1) if find a bracket keep it and check the second char

"""