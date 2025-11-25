#%%

import json

with open("Farfetch_products.json", "r") as f:
    products = json.load(f)

print(len(products))

def print_dicts_with_none_value(dict_list):
    for d in dict_list:
        if any(value is None for value in d.values()):
            print(d)

print_dicts_with_none_value(products)
