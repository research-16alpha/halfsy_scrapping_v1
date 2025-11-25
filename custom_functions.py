import re

def shop_simon_trim_product_image_links(**kwargs):
    for key, value in kwargs.items():
        if key == "brand" and value != "Shop Simon":
            return

        if key == "products" and value == list:
            products = kwargs[key]

    for product in products:
        text = product['product_image']
        match = re.search(r'url\((.*?)\)', text)
        if match:
            product['product_image'] = match.group(1)

    return products
