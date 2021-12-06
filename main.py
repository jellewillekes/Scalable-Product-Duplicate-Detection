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
    #print(f'Example of model (first model) and its descriptions elements: {models[0].keys()}')
    titles = helpers.get_titles(models)
    std_titles = helpers.std_titles(titles)
    return std_titles


def create_model_words(data):
    std_titles = clean_data(data)
    model_words = []
    for key in std_titles.keys():
        title_words = std_titles[key]
        for word in title_words:
            if word not in model_words:
                model_words.append(word)
    print(model_words)
    return model_words


if __name__ == '__main__':
    create_model_words(data)
