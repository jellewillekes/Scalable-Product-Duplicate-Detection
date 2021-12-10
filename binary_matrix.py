import re


def create_binary(data):
    # List of common count features.
    common_counts = ["Component", "HDMI", "USB", "Composite", "PC Input"]

    # For computational efficiency, we keep all model words as keys in a dictionary, where its value is the
    # corresponding row in the binary vector product representation.
    model_words = dict()
    binary_vec = []

    # Loop through all items to find model words.
    for i in range(len(data)):
        item = data[i]
        # Find model words in the title based on string, whitespace, bracket, alphanumeric characters
        mw_title = re.findall(
            "(?:^|(?<=[ \[\(]))([a-zA-Z0-9]*(?:(?:[0-9]+[^0-9\., ()]+)|(?:[^0-9\., ()]+[0-9]+)|(?:([0-9]+\.[0-9]+)["
            "^0-9\., ()]+))[a-zA-Z0-9]*)(?:$|(?=[ \)\]]))",
            item["title"])
        item_mw = []
        for match in mw_title:
            if match[0] != '':
                item_mw.append(match[0])
            else:
                item_mw.append(match[1])

        # Find model words in the key-value pairs.
        features = item["featuresMap"]
        for key in features:
            value = features[key]

            # Find decimals.
            # ([0-9]+\.[0-9]+) matches any (numeric) - . - (numeric) - (non-numeric) combination (i.e., decimals).
            # [a-zA-Z0-9]* matches any alphanumeric character (zero or more times).
            mw_decimal = re.findall("([0-9]+\.[0-9]+)[a-zA-Z]*", value)
            for decimal in mw_decimal:
                item_mw.append(decimal)

            # Group some common features.
            key_mw = key
            for feature in common_counts:
                if feature.lower() in key.lower():
                    key_mw = feature
                    break

            # Find the count value and construct a model word by appending the count to the key.
            if key in common_counts:
                counts = re.findall("^[0-9]+", value)
                for count in counts:
                    if count is not None:
                        item_mw.append(count + key_mw)

        # Loop through all identified model words and update the binary vector product representation.
        for mw in item_mw:
            if mw in model_words:
                # Set index for model word to one.
                row = model_words[mw]
                binary_vec[row][i] = 1
            else:
                # Add model word to the binary vector, and set index to one.
                binary_vec.append([0] * len(data))
                binary_vec[len(binary_vec) - 1][i] = 1

                # Add model word to the dictionary.
                model_words[mw] = len(binary_vec) - 1
    return binary_vec