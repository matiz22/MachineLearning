def calculate_gain(decision, entropies):
    return [decision - entropy for entropy in entropies]
