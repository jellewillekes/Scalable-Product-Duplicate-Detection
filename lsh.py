import sys
import numpy as np
import random
from sympy import nextprime


def minhash(binary_vec, n):

    random.seed()

    r = len(binary_vec)
    c = len(binary_vec[0])
    binary_vec = np.array(binary_vec)

    # Find k.
    k = nextprime(r - 1)

    # Generate n random hash functions.
    hash_params = np.empty((n, 2))
    for i in range(n):
        # Generate a, b, and k.
        a = random.randint(1, k - 1)
        b = random.randint(1, k - 1)
        hash_params[i, 0] = a
        hash_params[i, 1] = b

    signature = np.full((n, c), np.inf)

    # Loop through binary vector and calculate signature matrix
    for row in range(1, r + 1):
        # Compute each of the n random hashes once for each row.
        e = np.ones(n)
        row_vec = np.full(n, row)
        x = np.stack((e, row_vec), axis=1)
        row_hash = np.sum(hash_params * x, axis=1) % k

        for i in range(n):
            # Update column j if and only if it contains a one and its current value is larger than the hash value for
            updates = np.where(binary_vec[row - 1] == 0, np.inf, row_hash[i])
            signature[i] = np.where(updates < signature[i], row_hash[i], signature[i])
    return signature.astype(int)


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