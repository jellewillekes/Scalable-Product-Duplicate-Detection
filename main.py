import numpy as np
from math import comb

from clean_data import get_data, standardize_data, duplicates_matrix, calc_bin_vector #common_words
from minhash import minhash
from lsh import lsh

#'https://raw.githubusercontent.com/jwillekes18/duplicateDetection/master/TVs-all-merged.json'


def main():
    url = 'https://raw.githubusercontent.com/jwillekes18/ML-Porto-Seguro-s-Safe-Drive-Prediction/main/TVs-all-merged.json'
    data = get_data(url)

    std_data = standardize_data(data)

    #freq_words = common_words(std_data)
    #freq_words = freq_words[:15] # use 15 most frequent words for Binary Vector

    duplicates = duplicates_matrix(std_data)
    binary_vector = calc_bin_vector(std_data)
    n = round(round(0.5 * len(binary_vector)) / 100) * 100

    #Perform MinHashing
    signature_matrix = minhash(binary_vector, n)

    #Perform LSH with threshold at t=0.01
    t = 0.01
    candidates = lsh(signature_matrix, t)

    comparisons = np.sum(candidates)/2
    frac_of_comp = comparisons / comb(len(std_data), 2)

    correct = np.where(duplicates+candidates==2, 1, 0)
    n_correct = np.sum(correct)/2

    pq = n_correct / comparisons
    pc = n_correct / (np.sum(duplicates) / 2)

    f1_star = 2 * pq * pc / (pq + pc)

if __name__ == '__main__':
    main()
