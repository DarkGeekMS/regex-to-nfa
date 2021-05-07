# operations will be as following : and : 0 , or: 1 
import collections

def solveBracket(index, regex, states):
    pass

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
        elif regex[index] == '*':
            oring_end += 1
            states[oring_start].update({"ε" : oring_prev_char, "ε " : oring_end })
            states[oring_prev_char].update({"ε" : oring_end})
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
    # set the initial state to be "0" the value of each state consists of list such that, first element isTerminatingState , then the input to that state will lead to which state
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
            solveBracket(i, regex, states)
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
            states[start_state].update({"ε" : prev_char, "ε " : end_state })
            states[prev_char].update({"ε" : end_state})
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