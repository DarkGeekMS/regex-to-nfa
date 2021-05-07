

def solveBracket(index, regex, states):
    pass

def transform(regex):
    # set the initial state to be "0" the value of each state consists of list such that, first element isTerminatingState , then the input to that state will lead to which state
    states = { 0 : { "isTerminatingState": False } }
    #the state and end state to any expression in the regex
    start_state = 0
    end_state   = 0
    prev_start  = 0
    #start_bracket = False
    #prev_backSlash = False
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
            prev_start = start_state
            start_state = end_state
            i +=1
        # in case of open bracket solve the bracket in another function and update i and states in that function 
        elif regex[i] == '(':
            solveBracket(i, regex, states)
        # in case of oring 
        elif regex[i] == '|':
            i+=1
        # in case of repetition
        elif regex[i] == '*':
            end_state += 1
            states[start_state].update({"ε" : prev_start, "ε " : end_state })
            states[prev_start].update({"ε" : end_state})
            states.update( { end_state : { "isTerminatingState": False} })
            start_state = end_state
            i += 1
        else:
            # general case ( anding )
            end_state += 1
            states[start_state].update({regex[i] : end_state})
            states.update( { end_state : { "isTerminatingState": False } })
            prev_start = start_state
            start_state = end_state
            i += 1
    states[end_state]["isTerminatingState"] = True
    print(states)
    # loop over states and save them with the given example to json file
    # return that json file
    return None


"""
Assume i have input like that : "(A|B)C"
so we need to loop over each string : 
1) if find a bracket keep it and check the second char

"""