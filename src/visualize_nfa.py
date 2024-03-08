import graphviz

def visualize(nfa):
    # Initialize directed graph
    graph = graphviz.Digraph(comment='NFA Visualization')
    graph.graph_attr['rankdir'] = 'LR'  # Set graph flow from left to right
    graph.graph_attr['splines'] = 'polyline'  # Use straight lines
    graph.node('start', label='start', shape='plaintext')  # Set entry point

    # Get the starting state of NFA
    starting_state = nfa['startingState']
    del nfa['startingState']

    # Loop over each NFA state
    for state, transitions in nfa.items():
        # Construct a graph node for the state
        shape = 'doublecircle' if transitions['isFinalState'] else 'circle'
        
        # Choose color based on state
        if state == starting_state:
            color = 'yellow'
        elif transitions['isFinalState']:
            color = 'red'
        else:
            color = 'green'
        
        graph.node(state, label=state, shape=shape, fillcolor=color, style='filled')  # Add color to node

        # Check whether state is starting to draw input arrow
        if state == starting_state:
            graph.edge('start', state)

        # Loop over each successor state
        for successor, next_state in transitions.items():
            if successor != 'isFinalState':
                graph.edge(state, next_state, label=successor)

    # Set output format to SVG and render final graph
    graph.format = 'svg'
    graph.render('out/nfa-graph', view=True)
