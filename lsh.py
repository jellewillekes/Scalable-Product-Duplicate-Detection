import sys

import numpy as np


def lsh(signature, t):

    n = len(signature)

    # By Frasincar (2018), we use n = r*b for length of columns of signature matrix. Approx for the threshold is (1/b)^(1/r)
    r_best = 1
    b_best = 1
    best = 1
    for r in range(1, n + 1):
        for b in range(1, n + 1):
            if r * b == n:
                # Valid pair.
                approximation = (1 / b) ** (1 / r)
                if abs(approximation - t) < abs(best - t):
                    best = approximation
                    r_best = r
                    b_best = b

    candidates = np.zeros((len(signature[0]), len(signature[0])))
    for band in range(b_best):
        buckets = dict()
        start_row = r_best * band
        end_row = r_best * (band + 1)
        strings = ["".join(signature[start_row:end_row, column].astype(str)) for column in range(len(signature[0]))]
        ints = [int(string) for string in strings]
        hashes = [integer % sys.maxsize for integer in ints]

        # Add all item hashes to the correct bucket.
        for item in range(len(hashes)):
            hash_value = hashes[item]
            if hash_value in buckets:

                # All items already in this bucket are possible duplicates of this item.
                for candidate in buckets[hash_value]:
                    candidates[item, candidate] = 1
                    candidates[candidate, item] = 1
                buckets[hash_value].append(item)
            else:
                buckets[hash_value] = [item]
    return candidates.astype(int)