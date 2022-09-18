from itertools import chain, repeat, count, islice
from collections import Counter

# Taken from https://stackoverflow.com/questions/36429507/python-combinations-without-repetitions

def repeat_chain(values, counts):
    return chain.from_iterable(map(repeat, values, counts))


def unique_combinations_from_value_counts(values, counts, r):
    n = len(counts)
    indices = list(islice(repeat_chain(count(), counts), r))
    if len(indices) < r:
        return
    while True:
        yield tuple(values[i] for i in indices)
        for i, j in zip(reversed(range(r)), repeat_chain(reversed(range(n)), reversed(counts))):
            if indices[i] != j:
                break
        else:
            return
        j = indices[i] + 1
        for i, j in zip(range(i, r), repeat_chain(count(j), counts[j:])):
            indices[i] = j


def unique_combinations(iterable, r):
    values, counts = zip(*Counter(iterable).items())
    return unique_combinations_from_value_counts(values, counts, r)