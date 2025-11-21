#%%

import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from schema import ssense_schema, farfetch_schema, harrods_schema, doverstreetmarket_schema, sample_sale_schema, chicmi_schema, saks_schema, bloomingdales_schema, saks_pdp_schema

def extract_with_schema(html: str, schema: dict, base_url: str = "") -> list:
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

        # Include only meaningful results
        if any(v for v in item.values()):
            results.append(item)

    return results


import json
import os

def save_json(data, filename="extracted_data.json"):
    """Save structured data as a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Saved {len(data)} records to {filename}")

def main():
    all_products = []
    pages = [
        'internal_1.html'
    ]

    for page in pages:
        if not os.path.exists(page):
            print(f"❌ {page} not found, skipping.")
            continue

        with open(page, "r", encoding="utf-8") as f:
            html = f.read()

        try:
            products = extract_with_schema(
                html, saks_pdp_schema,
                base_url="https://www.saksfifthavenue.com"
            )
        except Exception as e:
            print(f"⚠️ Error extracting {page}: {e}")
            continue

        if not products:
            print(f"⚠️ No products found in {page}")
        else:
            all_products.extend(products)
            print(f"✅ Extracted {len(products)} products from {page}")

    if all_products:
        save_json(all_products, "saks_internal_page_bs4.json")    
    else:
        print("⚠️ No products extracted from any pages.")


if __name__ == "__main__":
    main()


