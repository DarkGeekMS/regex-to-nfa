import graphviz


def construct_node(state, nfa, starting_state, graph):
    # construct a graph node using given state
    # check whether state is terminal to draw double circle
    if nfa[state]['isTerminatingState']:
        graph.node(state, label=state, shape='doublecircle')
    else:
        graph.node(state, label=state, shape='circle')
    # check whether state is starting to draw input arrow
    if state == starting_state:
        graph.edge('start', state)


def visualize(nfa):
    # visualize output NFA into a directed graph
    # copy NFA dictionary
    nfa_copy = dict(nfa)
    # initialize directed graph
    graph = graphviz.Digraph(comment='NFA Visualization')
    # set graph flow from left to right
    graph.graph_attr['rankdir'] = 'LR'
    # set entry point
    graph.node('start', label='start', shape='plaintext')
    # get the starting state of NFA
    starting_state = nfa_copy['startingState']
    del nfa_copy['startingState']
    # initialize nodes list
    nodes = list()
    # loop over each NFA state
    for state in nfa_copy:
        # check whether state is created or not
        if not state in nodes:
            # add state to created nodes
            nodes.append(state)
            # construct a graph node for the state
            construct_node(state, nfa_copy, starting_state, graph)
        # loop over each successor state
        for successor in nfa_copy[state]:
            # skip 'isTerminatingState' key
            if successor != 'isTerminatingState':
                # check whether successor state is created or not
                if nfa_copy[state][successor] in nodes:
                    # create an edge between two states
                    graph.edge(state, nfa_copy[state][successor], label=successor)
                else:
                    # add state to created nodes
                    nodes.append(nfa_copy[state][successor])
                    # construct a graph node for the state
                    construct_node(nfa_copy[state][successor], nfa_copy, starting_state, graph)
                    # create an edge between two states
                    graph.edge(state, nfa_copy[state][successor], label=successor)
    # set output format to SVG
    graph.format = 'svg'
    # render final graph
    graph.render('out/nfa-graph', view=True)
