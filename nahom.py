import json
import pandas as pd
import time
import numpy as np
import csv
import re
import copy
from random import shuffle
from itertools import combinations
from clean_data import get_data

url = 'https://raw.githubusercontent.com/jwillekes18/ML-Porto-Seguro-s-Safe-Drive-Prediction/main/TVs-all-merged.json'
data = get_data(url)


def count_descriptions(data: dict) -> int:
    """Calculate number of descriptions of the dataset
    Args:
        data:   dictionary with lists of
    Returns:
        integer with total number of descriptions
    """
    descriptions = 0
    for key in data.keys():
        descriptions += len(data[key])
    return descriptions


def number_models(data: dict) -> dict:
    model = {}
    i = 0
    for key in data.keys():
        for description in data[key]:
            model[i] = description
            i += 1
    return model


def get_titles(models: dict) -> dict:
    titles = {}
    for key in models.keys():
        titles[key] = models[key]['title']
    return titles


def standardize_titles(titles: dict) -> dict:
    expr = '[a-zA-Z0-9.]*[0-9]+[a-zA-Z0-9.]*'
    for key in titles.keys():
        titles[key] = titles[key].replace('"', 'inch')
        titles[key] = titles[key].replace('Inch', 'inch')
        titles[key] = titles[key].replace('inches', 'inch')
        titles[key] = titles[key].replace('-inch', 'inch')
        titles[key] = titles[key].replace(' Inch', 'inch')
        titles[key] = titles[key].replace(' inch', 'inch')
        titles[key] = titles[key].replace('inch', 'inch')
        titles[key] = titles[key].replace('Hertz', 'hz')
        titles[key] = titles[key].replace('hertz', 'hz')
        titles[key] = titles[key].replace('Hz', 'hz')
        titles[key] = titles[key].replace('HZ', 'hz')
        titles[key] = titles[key].replace('-hz', 'hz')
        titles[key] = titles[key].replace(' hz', 'hz')
        titles[key] = titles[key].replace('hz', 'hz')
        titles[key] = titles[key].lower()
        titles[key] = re.sub("[^a-zA-Z0-9\s\.]", "", titles[key])
        titles[key] = re.findall(expr, titles[key])
    return titles


def describe_data(data):
    print(f'Description of the data:')
    print(f'Amount of keys in dataset: {len(data.keys())}')
    descriptions = count_descriptions(data)
    print(f'Total number of descriptions in keys: {descriptions}')
    return data


def clean_data(data):
    models = number_models(data)
    print(f'Example of model (first model) and its descriptions elements: {models[0].keys()}')
    titles = get_titles(models)
    std_titles = standardize_titles(titles)
    return std_titles


if __name__ == '__main__':
    describe_data(data)
    clean_data(data)

df = clean_data(data)
shingle_df = copy.deepcopy(df)

# create the vocabulary list to combine slinglings of all products to a vector set
vocab1 = set()
for i in shingle_df:
    vocab1 = set(vocab1.union(shingle_df[i]))
vocab_list = list(vocab1)
# vocab_list


# Converting the shingling to binary vector for all products
vocab_df = copy.deepcopy(df)
for i in vocab_df:
    vocab_df[i] = vocab_list
for i in vocab_df:
    vocab_df[i] = [1 if x in shingle_df[i] else 0 for x in vocab_df[i]]


# vocab_df


# Create functions for signature matrix
def create_hash_func(size: int):
    # function for creating the hash vector/function
    hash_ex = list(range(1, len(vocab_list) + 1))
    shuffle(hash_ex)
    return hash_ex  # here return the hashed permutaiton：（38，82，5，10，12，69，...）


def build_minhash_func(vocab_size: int, nbits: int):
    # function for building multiple minhash vectors
    hashes = []
    for _ in range(nbits):
        hashes.append(create_hash_func(vocab_size))
    return hashes


# we create 20 minhash vectors
minhash_func = build_minhash_func(len(vocab_list), 20)


def create_hash(vector: list):
    # use this function for creating our signatures (eg the matching)
    signature = []
    for func in minhash_func:
        for i in range(1, len(vocab_list) + 1):
            idx = func.index(i)
            signature_val = vector[idx]
            if signature_val == 1:
                signature.append(i)
                break
    return signature


# now create signatures
sig_df = copy.deepcopy(vocab_df)
for i in sig_df:
    sig_df[i] = create_hash(sig_df[i])


# Perform the LSH, create the LSH functions
def split_vector(signature, b):
    assert len(signature) % b == 0  # reminder must be zero
    r = int(len(signature) / b)
    # code splitting signature in b parts
    subvecs = []
    for i in range(0, len(signature), r):
        subvecs.append(signature[i: i + r])
    return subvecs


# Band IS B = 10
band_df = copy.deepcopy(sig_df)
for i in band_df:
    band_df[i] = split_vector(band_df[i], 10)

# Locality-Sensitive Hashing and return the candidate pair.
for key1, key2 in combinations(band_df.keys(), r=2):
    for i_rows, j_rows in zip(band_df[key1], band_df[key2]):
        if i_rows == j_rows:
            print(f"Candidate pair: {key1, key2} {i_rows} == {j_rows}")