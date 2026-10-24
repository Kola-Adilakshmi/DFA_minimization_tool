
def minimize_dfa(states, alphabet, start, final_states, transitions):
    # Find states reachable from the start state.
    reachable = set()
    pending = [start]

    while pending:
        state = pending.pop()

        if state in reachable:
            continue

        reachable.add(state)

        for symbol in alphabet:
            destination = transitions[(state, symbol)]

            if destination not in reachable:
                pending.append(destination)

    states = [state for state in states if state in reachable]
    final_states = set(final_states) & set(states)
    non_final_states = set(states) - final_states

    # Initial partition: final and non-final states.
    partitions = []

    if final_states:
        partitions.append(final_states)

    if non_final_states:
        partitions.append(non_final_states)

    # Repeatedly split partitions until stable.
    while True:
        changed = False
        new_partitions = []

        for group in partitions:
            groups_by_signature = {}

            for state in group:
                signature = tuple(
                    next(
                        i for i, partition in enumerate(partitions)
                        if transitions[(state, symbol)] in partition
                    )
                    for symbol in alphabet
                )

                groups_by_signature.setdefault(
                    signature, set()
                ).add(state)

            new_partitions.extend(groups_by_signature.values())

            if len(groups_by_signature) > 1:
                changed = True

        partitions = new_partitions

        if not changed:
            break

    # Give each equivalence class a new state name.
    partitions.sort(
        key=lambda group: (
            0 if start in group else 1,
            sorted(group)[0]
        )
    )

    state_names = {}
    for index, group in enumerate(partitions):
        name = f"M{index}"
        for state in group:
            state_names[state] = name

    minimized_states = [
        f"M{i}" for i in range(len(partitions))
    ]

    minimized_start = state_names[start]
    minimized_finals = {
        state_names[state] for state in final_states
    }

    minimized_transitions = {}

    for index, group in enumerate(partitions):
        representative = next(iter(group))
        new_state = f"M{index}"

        for symbol in alphabet:
            destination = transitions[(representative, symbol)]
            minimized_transitions[(new_state, symbol)] = (
                state_names[destination]
            )

    return (
        minimized_states,
        minimized_start,
        minimized_finals,
        minimized_transitions,
        partitions
    )


def main():
    print("DFA MINIMIZATION TOOL")
    print("=" * 45)

    states = input(
        "Enter states separated by commas (e.g. A,B,C,D): "
    ).replace(" ", "").split(",")

    alphabet = input(
        "Enter alphabet symbols separated by commas (e.g. 0,1): "
    ).replace(" ", "").split(",")

    start = input("Enter the start state: ").strip()

    final_states = set(
        input("Enter final states separated by commas: ")
        .replace(" ", "").split(",")
    )

    if not final_states or final_states == {""}:
        final_states = set()

    if len(set(states)) != len(states):
        raise ValueError("State names must be unique.")

    if len(set(alphabet)) != len(alphabet):
        raise ValueError("Alphabet symbols must be unique.")

    if not states or not alphabet:
        raise ValueError("States and alphabet cannot be empty.")

    if start not in states:
        raise ValueError("Start state must be in the state list.")

    if not final_states.issubset(set(states)):
        raise ValueError("Every final state must be in the state list.")

    transitions = {}

    print("\nEnter the destination for each transition.")

    for state in states:
        for symbol in alphabet:
            destination = input(
                f"Transition from {state} on {symbol}: "
            ).strip()

            if destination not in states:
                raise ValueError(
                    f"Unknown destination state: {destination}"
                )

            transitions[(state, symbol)] = destination

    (
        minimized_states,
        minimized_start,
        minimized_finals,
        minimized_transitions,
        partitions
    ) = minimize_dfa(
        states, alphabet, start, final_states, transitions
    )

    print("\nORIGINAL DFA")
    print("-" * 45)
    print("States:", states)
    print("Start state:", start)
    print("Final states:", sorted(final_states))

    print("\nMINIMIZED DFA")
    print("-" * 45)
    print("States:", minimized_states)
    print("Start state:", minimized_start)
    print("Final states:", sorted(minimized_finals))

    print("\nEquivalent state groups:")
    for index, group in enumerate(partitions):
        print(f"M{index} = {{{', '.join(sorted(group))}}}")

    print("\nMINIMIZED TRANSITION TABLE")
    print("-" * 45)
    print("State\t" + "\t".join(alphabet))

    for state in minimized_states:
        destinations = [
            minimized_transitions[(state, symbol)]
            for symbol in alphabet
        ]
        print(state + "\t" + "\t".join(destinations))

    print("\nOriginal state count:", len(states))
    print("Reachable state count:", len(set(
        state for group in partitions for state in group
    )))
    print("Minimized state count:", len(minimized_states))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as error:
        print("Input error:", error)
