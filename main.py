import numpy as np
from math import comb
import matplotlib.pyplot as plt

from clean_data import get_data, standardize_data, duplicates_matrix, calc_bin_vector
from lsh import lsh, minhash

'https://raw.githubusercontent.com/jwillekes18/duplicateDetection/master/TVs-all-merged.json'


def main():
    url = 'https://raw.githubusercontent.com/jwillekes18/duplicateDetection/master/TVs-all-merged.json'
    data = get_data(url)

    std_data = standardize_data(data)

    #freq_words = common_words(std_data)
    #freq_words = freq_words[:15] # use 15 most frequent words for Binary Vector

    duplicates = duplicates_matrix(std_data)
    binary_vector = calc_bin_vector(std_data)

    # number of hash function is 50% o fthe size of binary signature vector. k is half of the value of r/
    n = round(round(0.5 * len(binary_vector)) / 100) * 100

    #Perform MinHashing
    signature_matrix = minhash(binary_vector, n)

    #Perform LSH with threshold at t=0.01
    thresholds = [0.01, 0.05, 0.1, 0.20, 0.5, 0.9]

    comparisons_total = []
    frac_of_comp_total = []
    pq_total = []
    pc_total = []
    f1_star_total = []

    for t in thresholds:
        print("t = ", t)
        candidates = lsh(signature_matrix, t)
        comparisons = np.sum(candidates) / 2
        frac_of_comp = comparisons / comb(len(std_data), 2)

        correct = np.where(duplicates + candidates == 2, 1, 0)
        n_correct = np.sum(correct) / 2

        pq = n_correct / comparisons
        pc = n_correct / (np.sum(duplicates) / 2)

        f1_star = 2 * pq * pc / (pq + pc)

        comparisons_total.append(comparisons)
        frac_of_comp_total.append(frac_of_comp)
        #pq_total = pq_total.append(pq)
        #pc_total = pc_total.append(pc)
        #f1_star_total = f1_star_total.append(f1_star)
        print(comparisons, frac_of_comp, pq, pc, f1_star)

    #plt.figure(figsize=(20,10))
    #plt.plot(comparisons_total, f1_star_total)
    #plt.xlabel('Fraction comparisons')
    #plt.ylabel('F1*')
    #plt.show()


if __name__ == '__main__':
    main()
