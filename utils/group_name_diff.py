from difflib import SequenceMatcher


def similar(name, original_name):
    return SequenceMatcher(None, name, original_name).ratio()
