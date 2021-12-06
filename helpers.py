import numpy as np
import pandas as pd


def count_descriptions(data: dict)->int:
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

def number_desc