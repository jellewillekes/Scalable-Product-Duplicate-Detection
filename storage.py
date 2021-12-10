
    thresholds = [1]
    bootstraps = 1

    for t in thresholds:
        print("t = ", t)
        results = np.zeros(4)

        for b in range(bootstraps):
            data_sample, duplicates_sample = bootstrap(clean_list, duplicates)
            comparisons_run, pq_run, pc_run, f1_star_run = perform_lsh(data_sample, duplicates_sample, t)
            results += np.array([comparisons_run, pq_run, pc_run, f1_star_run])

        statistics = results/bootstraps
    print(statistics)


def perform_lsh(clean_list, duplicates, t):
    binary_vec = create_binary(clean_list)
    n = round(round(0.5 * len(binary_vec)) / 100) * 100
    signature = minhash(binary_vec, n)
    candidates = lsh(signature, t)

    # Compute number of comparisons.
    comparisons = np.sum(candidates) / 2
    comparison_frac = comparisons / comb(len(clean_list), 2)

    # Compute matrix of correctly binned duplicates, where element (i, j) is equal to one if incident i and incident j are
    # duplicates, and correctly classified as such by LSH.
    correct = np.where(duplicates + candidates == 2, 1, 0)
    n_correct = np.sum(correct) / 2

    # Compute Pair Quality (PQ)
    pq = n_correct / comparisons

    # Compute Pair Completeness (PC)
    pc = n_correct / (np.sum(duplicates) / 2)

    # Compute F_1^* measure.
    f1_star = 2 * pq * pc / (pq + pc)

    # Cluster and compute F_1 measure.
    #tp, precision = cluster(clean_list, candidates, duplicates)
    #recall = tp / (np.sum(duplicates) / 2)
    #f1 = 2 * precision * recall / (precision + recall)

    return comparison_frac, pq, pc, f1_star


def bootstrap(data_list, duplicates):
    # Compute indices to be included in the bootstrap.
    indices = [random.randint(x, len(data_list) - 1) for x in [0] * len(data_list)]

    # Collect samples.
    data_sample = [data_list[index] for index in indices]
    duplicates_sample = np.take(np.take(duplicates, indices, axis=0), indices, axis=1)
    return data_sample, duplicates_sample





    model_words = dict()
    bin_vector = []

    for i in range(len(std_data)):
        model = std_data[i]
        model_title = re.findall("(?:^|(?<=[ \[\(]))([a-zA-Z0-9]*(?:(?:[0-9]+[^0-9\., ()]+)|(?:[^0-9\., ()]+[0-9]+)|(?:([0-9]+\.[0-9]+)["
            "^0-9\., ()]+))[a-zA-Z0-9]*)(?:$|(?=[ \)\]]))", model['title'])
        incident_mw = []
        for match in model_title:
            if match[0] != '':
                incident_mw.append(match[0])
            else:
                incident_mw.append(match[1])

    for mw in incident_mw:
        if mw in model_words:
            row = model_words[mw]
            bin_vector[row][i] = 1
        else:
            bin_vector.append([0]*len(std_data))
            bin_vector[len(bin_vector) -1][i] = 1

            model_words = len(bin_vector) -1
    return  bin_vector