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

    # Initialize signature matrix to infinity for each element.
    signature = np.full((n, c), np.inf)

    # Loop through the binary vector representation matrix once, to compute the signature matrix.
    for row in range(1, r + 1):
        # Compute each of the n random hashes once for each row.
        e = np.ones(n)
        row_vec = np.full(n, row)
        x = np.stack((e, row_vec), axis=1)
        row_hash = np.sum(hash_params * x, axis=1) % k

        for i in range(n):
            # Update column j if and only if it contains a one and its current value is larger than the hash value for
            # the signature matrix row i.
            updates = np.where(binary_vec[row - 1] == 0, np.inf, row_hash[i])
            signature[i] = np.where(updates < signature[i], row_hash[i], signature[i])
    return signature.astype(int)