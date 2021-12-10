import re
import numpy as np
import requests
import json


def get_data(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data


def count_models(data):
    models = 0
    i = 0
    for model in data.keys():
        models += len(data[model])
    return models


def standardize_data(data):
    # Declare common value representations to be replaced by the last value of the list.
    #expr = '[a-zA-Z0-9.]*[0-9]+[a-zA-Z0-9.]*'

    # Standardize Data.
    std_data = []
    for modelID in data:
        for incident in data[modelID]:
            incident['title'] = incident['title'].replace('"', 'inch')
            incident['title'] = incident['title'].replace('inches', 'inch')
            incident['title'] = incident['title'].replace('-inch', 'inch')
            incident['title'] = incident['title'].replace('Hertz', 'hz')
            incident['title'] = incident['title'].replace('-hz', 'hz')
            incident['title'] = incident['title'].lower()
            incident['title'] = re.sub("[^a-zA-Z0-9\s\.]","", incident['title']) #remove non-alphabetical characters

    # Standardize features
            for feature in incident["featuresMap"]:
                incident["featuresMap"][feature] = incident["featuresMap"][feature].replace('"', 'inch')
                incident['title'] = incident['title'].replace('inches', 'inch')
                incident['title'] = incident['title'].replace('-inch', 'inch')
                incident['title'] = incident['title'].replace('Hertz', 'hz')
                incident['title'] = incident['title'].replace('-hz', 'hz')
                incident["featuresMap"][feature] = incident["featuresMap"][feature].lower()
                incident["featuresMap"][feature] = re.sub("[^a-zA-Z0-9\s\.]","", incident["featuresMap"][feature])
            std_data.append(incident)

    return std_data


def duplicates_matrix(std_data):
    # Set all values zero initially and add 1 if row and column correspond
    duplicates = np.zeros((len(std_data), len(std_data)))
    for row in range(len(std_data)):
        model_row = std_data[row]["modelID"]
        for col in range(row + 1, len(std_data)):
            model_col = std_data[col]["modelID"]
            if model_row == model_col:
                duplicates[row][col] = 1
                duplicates[col][row] = 1

    return duplicates.astype(int)


def calc_bin_vector(std_data):
    # List of common count features.
    freq_words = ["Aspect Ratio", "UPC", "HDMI", "Component", "Video", "Contrast", "Composite", "Speakers", "HDMI", "USB"]

    model_words = dict()
    binary_vec = []

    # Loop through all incidents to find model words.
    for i in range(len(std_data)):
        incident = std_data[i]
        model_title = re.findall(
            "(?:^|(?<=[ \[\(]))([a-zA-Z0-9]*(?:(?:[0-9]+[^0-9\., ()]+)|(?:[^0-9\., ()]+[0-9]+)|(?:([0-9]+\.[0-9]+)["
            "^0-9\., ()]+))[a-zA-Z0-9]*)(?:$|(?=[ \)\]]))",
            incident["title"])
        incident_mw = []
        for match in model_title:
            if match[0] != '':
                incident_mw.append(match[0])
            else:
                incident_mw.append(match[1])

        # Find model words in the key-value pairs.
        features = incident["featuresMap"]
        for key in features:
            value = features[key]

            # Find decimals.
            # ([0-9]+\.[0-9]+) matches any (numeric) - . - (numeric) - (non-numeric) combination (i.e., decimals).
            # [a-zA-Z0-9]* matches any alphanumeric character (zero or more times).
            mw_decimal = re.findall("([0-9]+\.[0-9]+)[a-zA-Z]*", value)
            for decimal in mw_decimal:
                incident_mw.append(decimal)

            # Group some common features.
            key_mw = key
            for feature in freq_words:
                if feature.lower() in key.lower():
                    key_mw = feature
                    break

            # Find the count value and construct a model word by appending the count to the key.
            if key in freq_words:
                counts = re.findall("^[0-9]+", value)
                for count in counts:
                    if count is not None:
                        incident_mw.append(count + key_mw)

        # Loop through all identified model words and update the binary vector product representation.
        for mw in incident_mw:
            if mw in model_words:
                # Set index for model word to one.
                row = model_words[mw]
                binary_vec[row][i] = 1
            else:
                # Add model word to the binary vector, and set index to one.
                binary_vec.append([0] * len(std_data))
                binary_vec[len(binary_vec) - 1][i] = 1

                # Add model word to the dictionary.
                model_words[mw] = len(binary_vec) - 1
    return binary_vec

"""
def common_words(data):
    feature_count = dict()

    # Find words that are most frequently used. We can use it for the key value pairs when creating binary vector
    for i in range(len(data)):
        incident = data[i]
        features = incident["featuresMap"]

        for key in features:
            value = features[key]

            count = re.match("^[0-9]+$", value)
            if count is not None:
                if key in feature_count:
                    feature_count[key] += 1
                else:
                    feature_count[key] = 1
    freq_words = [(value, key) for key, value in feature_count.keys()]
    freq_words.sort(reverse=True)
    return freq_words
"""