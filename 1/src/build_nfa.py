import collections
import json

def solveBracket(regex, end_state, states):
    """
        This function used to solve the regex inside a bracket and save the new states to the current available states
    """

    # initialization for the new states to be created must start with the last created state + 1
    b_start = end_state + 1
    b_prev = end_state + 1
    b_char = end_state + 1
    b_end = end_state + 1
    # create new state to indicate we are working with bracket regex
    states.update( { b_end : { "isTerminatingState": False } })
    # start looping over the regex inside the bracket to transform it
    index = 0
    while(index < len(regex)):
        # in case of oring operation found 
        if regex[index] == '|':
            # solve it using oring function (function description below) 
            index, prev, start,end = oring(index+1, regex, states , b_end)
            # create new 2 states to connect the oring branches
            states.update( { end+1 : { "isTerminatingState": False, "ε" : b_prev , "ε " : prev } })
            states.update( { end+2 : { "isTerminatingState": False} })
            states[end].update({"ε" : end+2})
            states[b_end].update({"ε" : end+2})
            #update the indices used to loop in states
            b_char = end + 1
            b_end = end +2
            b_start = b_end
            b_prev = end + 1
        # in case of new bracket found
        elif regex[index] == '(':
            # get the regex inside that bracket
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
            # then solve it using this function recursively
            prev , start, end = solveBracket(sub_regex, b_end, states) 
            # connect the new bracket regex with the current one with epsilon state
            states[b_end].update({"ε" : prev})
            b_end = end
            b_start = b_end
            b_char = prev
            # update the current index to start after the solved bracket
            index = index + len(sub_regex) + 1
        # in case of special character found
        elif regex[index] == '\\':
            # read the charactr after the \ and make a normal transition from the current state to new one using that character
            index += 1
            states[b_end].update({regex[index] : (b_end+1)})
            b_end +=1
            states.update( { b_end : { "isTerminatingState": False } })
            b_char = b_start
            b_start = b_end
        # in case of partitioning found
        elif regex[index] == '*':
            # create two states using tompthons rules as described in the slides
            b_end += 1
            states[b_start].update({" ε " : b_char, "  ε  " : b_end })
            states[b_char].update({"ε            " : b_end})
            states.update( { b_end : { "isTerminatingState": False} })
            b_start = b_end
        # in case of anding
        else:
            # make new state and new transaction from the current state to the new one using that char in the regex
            b_end +=1
            states[b_start].update( { regex[index] : b_end })
            states.update( { b_end : { "isTerminatingState": False } })
            b_char = b_start
            b_start = b_end    
        # increment the regex looping index     
        index += 1          
    # return information about the states added by this function when it's called     
    return b_prev, b_start, b_end

def oring(index , regex, states , end_state):
    """
        This function used to solve the regex after or operation and save the new states to the current available states
    """

    # initialization for the new states to be created must start with the last created state + 1
    oring_start = end_state + 1
    oring_prev = end_state + 1
    oring_prev_char = end_state + 1
    oring_end = end_state + 1
    # create new state to indicate we are working with bracket regex
    states.update( { oring_end : { "isTerminatingState": False } })

    # loop over the regex
    while(index < len(regex)):
        # in case of oring so the regex after oring operation was solved so return its states
        if regex[index] == '|':
            return (index), oring_prev, oring_start, oring_end
        # in case of special character found
        elif regex[index] == '\\':
            # take the next character after \ 
            index += 1
            oring_end +=1
            # make a transition from the current state to new one using that character
            states[oring_start].update({regex[index] : (oring_end)})
            states.update( { oring_end : { "isTerminatingState": False } })
            # update states indeces
            oring_prev_char = oring_start
            oring_start = oring_end
        # in case of bracket found
        elif regex[index] == '(':
            # get the regex inside that bracket
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
            # solve that regex using the bracket solver function
            prev , start, end = solveBracket(sub_regex, oring_end, states) 
            # connect the resulting states with the current state using one spsilon move
            states[oring_end].update({"ε" : prev})
            # update the states indeces
            oring_end = end
            oring_start = oring_end
            oring_prev_char = prev
            # continue looping over the regex after that bracket
            index = index + len(sub_regex) + 1
        # in case of repition found
        elif regex[index] == '*':
            # create two state and connect between them using tompthon rule as decribed in the slides
            oring_end += 1
            states[oring_start].update({"   ε   " : oring_prev_char, "     ε     " : oring_end })
            states[oring_prev_char].update({"ε        " : oring_end})
            states.update( { oring_end : { "isTerminatingState": False} })
            oring_start = oring_end
        # in case of anding 
        else:
            # make a transition from the current state to new state using that input
            oring_end +=1
            states[oring_start].update( { regex[index] : oring_end })
            states.update( { oring_end : { "isTerminatingState": False } })
            oring_prev_char = oring_start
            oring_start = oring_end   
        # update the regex counter to continue looping over it      
        index += 1        
    # return information about the states added by this function when it's called     
    return len(regex), oring_prev, oring_start, oring_end

def transform(regex):
    # create initial state
    states = { 0 : { "isTerminatingState": False } }
    #the state and end state to any expression in the regex
    start_state = 0
    end_state   = 0
    prev_char = 0
    prev_start  = 0
    n = len(regex)
    i = 0
    while i < n:
        # in case of special character found
        if regex[i] == '\\' :
            # take the next character after \ 
            i += 1
            # make a transition from the current state to new one using that character
            end_state += 1
            states[start_state].update({regex[i] : end_state})
            states.update( { end_state : { "isTerminatingState": False } })
            prev_char = start_state
            start_state = end_state
            # update the regex counter to continue looping over it  
            i +=1
        # in case of open bracket solve the bracket in another function and update i and states in that function 
        elif regex[i] == '(':
            # get the regex inside that bracket
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
            # solve that regex using the bracket solver function
            prev , start, end = solveBracket(sub_regex, end_state, states) 
            # connect the resulting states with the current state using one spsilon move
            states[end_state].update({"ε" : prev})
            # update the states indeces
            end_state = end
            start_state = end_state
            prev_char = prev
            # continue looping over the regex after that bracket
            i = i + len(sub_regex) + 2
        # in case of oring 
        elif regex[i] == '|':
            # solve it using oring function (function description above) 
            i, prev, start,end = oring(i+1, regex, states , end_state)
            # create new 2 states to connect the oring branches
            states.update( { end+1 : { "isTerminatingState": False, "     ε     " : prev_start , "      ε       " : prev } })
            states.update( { end+2 : { "isTerminatingState": False} })
            states[end].update({"ε" : end+2})
            states[end_state].update({"ε" : end+2})
            #update the state indices 
            prev_char = end + 1
            end_state = end +2
            start_state = end_state
            prev_start = end + 1
        # in case of repetition
        elif regex[i] == '*':
            # create two state and connect between them using tompthon rule as decribed in the slides
            end_state += 1
            states[start_state].update({"ε   " : prev_char, "ε    " : end_state })
            states[prev_char].update({"ε     " : end_state})
            states.update( { end_state : { "isTerminatingState": False} })
            start_state = end_state
            # update the regex counter to continue looping over it  
            i += 1
        # in case of anding
        else:
            # make a transition from the current state to new state using that input
            end_state += 1
            states[start_state].update({regex[i] : end_state})
            states.update( { end_state : { "isTerminatingState": False } })
            prev_char = start_state
            start_state = end_state
            # update the regex counter to continue looping over it  
            i += 1

    # make the last state as out state
    states[end_state]["isTerminatingState"] = True
    # sort the state ascending
    states = collections.OrderedDict(sorted(states.items()))
    # printing the states for debugging
    #for k, v in states.items(): print(k, v)

    # loop over sorted states and save them as the given example to json file
    # return the json file content to be displayed in graph format
    results = {}
    results.update({"startingState" : ("S" + str(prev_start))})
    for key , value in states.items():
        entry = {}
        for k,v in value.items():
            if k == "isTerminatingState":
                entry.update({k : v})
            else:
               entry.update(({k : ("S" + str(v))})) 
        results.update({("S"+ str(key)) : entry})
    with open('out/nfa.json', 'w') as fp:
        json.dump(results, fp, ensure_ascii=False)
    return results
