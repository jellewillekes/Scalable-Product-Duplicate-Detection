# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import requests
import json

import helpers

url = 'https://raw.githubusercontent.com/jwillekes18/duplicateDetection/master/TVs-all-merged.json'

def describe_data(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    print(f'Important output for understanding the data and code below:')
    print(f'Amount of keys in dataset: {len(data.keys())}')
    descriptions = helpers.count_descriptions(data)
    print(f'Total number of descriptions in keys: {descriptions}')
    return data

def clean_data(data):



    return

if __name__ == '__main__':
    describe_data(url)

