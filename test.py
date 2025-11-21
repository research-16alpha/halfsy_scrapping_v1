#%%

import json

with open('Saks Fifth Avenue_products.json', 'r') as f:
    data = json.load(f)

len(data)