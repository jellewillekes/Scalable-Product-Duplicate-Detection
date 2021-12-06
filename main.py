import numpy as np
import requests
import json

import helpers

#'https://raw.githubusercontent.com/jwillekes18/duplicateDetection/master/TVs-all-merged.json'

url = 'https://raw.githubusercontent.com/jwillekes18/ML-Porto-Seguro-s-Safe-Drive-Prediction/main/TVs-all-merged.json'
resp = requests.get(url)
data = json.loads(resp.text)


def describe_data(data):
    print(f'Description of the data:')
    print(f'Amount of keys in dataset: {len(data.keys())}')
    descriptions = helpers.count_descriptions(data)
    print(f'Total number of descriptions in keys: {descriptions}')
    return data


def clean_data(data):
    models = helpers.number_models(data)
    print(f'Example of model (first model) and its descriptions elements: {models[0].keys()}')
    titles = helpers.get_titles(models)
    std_titles = helpers.standardize_titles(titles)
    return std_titles


if __name__ == '__main__':
    describe_data(data)
    clean_data(data)

