"""
A set of helper functions for the main script.

Author: Dmytro Kuksenko
Date: Sept 14, 2022

"""

import numpy as np

# The idea behind the infer_spaces function implementation is from [1]
# [1] https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words

words = open("data\dictionary.dat").read().split()
wordcost = dict((k, np.log((i + 1) * np.log(len(words)))) for i, k in enumerate(words))
maxword = max(len(x) for x in words)


def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - maxword) : i]))
        return min(
            (c + wordcost.get(s[i - k - 1 : i], 9e999), k + 1) for k, c in candidates
        )

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k : i])
        i -= k

    return " ".join(reversed(out))
