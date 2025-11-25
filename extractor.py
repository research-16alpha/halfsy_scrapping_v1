#%%

import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import re
from productClassification import classify_products_bulk
from datetime import datetime
from zoneinfo import ZoneInfo
from schema import *
from custom_functions import shop_simon_trim_product_image_links

def extract_products_with_schema(html: str, schema: dict, base_url: str = "") -> list:
    """
    Schema-based HTML extractor using BeautifulSoup.
    You define selectors and data types in `schema`.
    Returns list of extracted dicts.
    """

    soup = BeautifulSoup(html, "html.parser")
    base_selector = schema.get("baseSelector", "body")
    base_elements = soup.select(base_selector)
    results = []

    for element in base_elements:
        item = {}
        for field in schema.get("fields", []):
            name = field.get("name")
            selector = field.get("selector")
            ftype = field.get("type", "text")
            attr = field.get("attribute")

            target = element.select_one(selector) if selector else element

            if not target:
                item[name] = None
                continue

            # Extraction logic
            if ftype == "text":
                value = target.get_text(strip=True)
            elif ftype == "attribute" and attr:
                value = target.get(attr)
                if name.lower().endswith("link") and base_url:
                    value = urljoin(base_url, value)
            elif ftype == "html":
                value = str(target)
            elif ftype == "json":
                try:
                    value = json.loads(target.get_text())
                except:
                    value = None
            else:
                value = None

            item[name] = value

        item = _update_discount(item)
        item = _update_scraping_time(item)
        
        # Include only meaningful results
        if any(v for v in item.values()):
            results.append(item)

        
    return results

def _update_scraping_time(product: dict):
    ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    formatted_ist = ist_time.strftime("%Y-%m-%d %H:%M:%S")
    product["scraped_at"] = formatted_ist
    return product

def _to_number(value):
    """
    Convert a messy price string into a float.
    
    Handles:
    - Currency symbols ($, €, £, ₹, ¥, etc.)
    - Commas
    - Text before/after (e.g., 'USD 1,299.50', 'Price: $200')
    - Values with no symbol
    - Values like '€ 1 200'
    """

    if not value:
        return None
    
    if not isinstance(value, str):
        # Already numeric (int/float)
        try:
            return float(value)
        except:
            return None

    # 1. Extract the FIRST number-like token using regex
    # Supports formats:
    # - 1,299.50
    # - 1299,50 (European)
    # - 1299
    # - 1 299
    pattern = r'[\d\.,\s]+'
    match = re.search(pattern, value)
    if not match:
        return None

    num_str = match.group(0)

    # 2. Remove spaces
    num_str = num_str.replace(" ", "")

    # 3. If it uses comma as decimal separator (European format: "1299,50")
    if num_str.count(",") == 1 and num_str.count(".") == 0:
        num_str = num_str.replace(",", ".")

    # 4. Remove thousand separators ","
    num_str = num_str.replace(",", "")

    # 5. Convert to float
    try:
        return float(num_str)
    except:
        return None

def _update_discount(product: dict):
    original_price = _to_number(product.get("original_price"))
    sale_price = _to_number(product.get("sale_price"))

    if not original_price or not sale_price:
        product["discount"] = None
        return product

    discount = (original_price - sale_price) / original_price
    product["discount"] = f"{int(discount * 100)}%"
    return product


def save_json(data, filename="extracted_data.json"):
    """Save structured data as a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Saved {len(data)} records to {filename}")

def main():
    products = []
    page = "bloomingdates.html"

    print(f"⏰Reading HTML file : {page}")
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()
    print(f"Successfully read HTML file😘")

    try:
        print(f"⏰Extracting products from HTML file")
        products = extract_products_with_schema(
            html, bloomingdales_schema,
            base_url="https://www.bloomingdales.com"
        )
        print(f"Successfully Extracted {len(products)} products from HTML file😘")
        
        print(f"⏰Classifying products")
        products = classify_products_bulk(products, product_key="product_name")
        print(f"Successfully Classified {len(products)} products😘")

        print(f"⏰Saving products to JSON file")
        save_json(products, filename="bloomingdales_products.json")
        print(f"✅ Saved {len(products)} products to JSON file")

    except Exception as e:
        print(f"😭 Error extracting {page}: {e}")
    
    if not products:
        print(f"😭 No products found in {page}")
    else:
        print(f"✅ Extracted {len(products)} products from {page}")

if __name__ == "__main__":
    main()

#%%

with open('Shop Simon_products.json', 'r') as f:
    products = json.load(f)

brand = "Shop Simon"

prods = shop_simon_trim_product_image_links(brand=brand, products=products)

