from colorama import init, Fore         # colorize the terminal output

def table(nfa):

    # initialize colorama
    init(autoreset=True)

    # Get all unique input symbols from the NFA
    input_symbols = set()
    for state, transitions in nfa.items():
        for symbol in transitions.keys():
            if symbol.strip() != 'isFinalState':
                input_symbols.add(symbol.strip())
    input_symbols = sorted(list(input_symbols))  # Sort for consistent column order

    # Initialize transition table with empty strings
    transition_table = {state: {symbol: [] for symbol in input_symbols} for state in nfa.keys()}

    # Fill in transition table with next states
    for state, transitions in nfa.items():
        for symbol, next_states in transitions.items():
            if symbol.strip() != 'isFinalState':
                # Append next state to the corresponding symbol list
                transition_table[state][symbol.strip()].extend([ns.strip() for ns in next_states.split(',')])

    # Calculate maximum width for each column
    col_widths = [max(len(state), max(len(', '.join(transitions[symbol])) for state, transitions in transition_table.items())) for symbol in input_symbols]

    # Print transition table
    print()
    state_color = Fore.BLUE
    print(f'| {state_color}State', end='')
    for symbol, width in zip(input_symbols, col_widths):
        print(f'\t| {state_color}{symbol.center(width)}{Fore.RESET}', end='')
    print('\t|')
    
    # coloring the table according to the transition diagram
    for state, transitions in transition_table.items():
        if state == 'S0':
            # Initial state (yellow)
            state_color = Fore.YELLOW
        elif any(next_states for next_states in transitions.values()):
            # Intermediate states (green)
            state_color = Fore.GREEN
        else:
            # Final state (red)
            state_color = Fore.RED

        print(f'| {state_color}{state}{Fore.RESET}', end='')
        for symbol, width in zip(input_symbols, col_widths):
            next_states = ', '.join(transitions[symbol])
            next_states = " Φ " if not next_states else next_states  # Replace empty cells with "phi"
            print(f'\t| {next_states.center(width)}', end='')
        print('\t|')
    print()
