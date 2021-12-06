import numpy as np
import pandas as pd
import re

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
        titles[key] = titles[key].replace('"','inch')
        titles[key] = titles[key].lower()
        titles[key] = re.sub("[^a-zA-Z0-9\s\.]","", titles[key])
        titles[key] = re.findall(expr, titles[key])
    return titles

