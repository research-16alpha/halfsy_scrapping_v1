
from productClassification import classify_products_bulk
from extractor import extract_products_with_schema, save_json
from database import insert_data
from optimised_async_scrape import *
from proxies import *
from metadata import WEBSITES
from schema import *
from links import *
from base_links import *
from custom_functions import shop_simon_trim_product_image_links

async def main(brand, schema, base_url, urls):

    CONCURRENCY_LIMIT = 2

    print(f"⏰Scraping {len(urls)} pages")
    html_list = await scrape_multiple(urls=urls, concurrency_limit=CONCURRENCY_LIMIT, proxies = PROXIES)
    print(f"✅ Successfully scraped {len(html_list)} pages")

    print(f"⏰Extracting products")
    all_products = []
    for html in html_list:
        
        print(f"⏰Extracting products from {html_list.index(html) + 1} html file of {len(html_list)} html files")
        products = extract_products_with_schema(html=html, schema = schema, base_url = base_url)
        print(f"✅ Successfully extracted {len(products)} products")
        
        print(f"⏰Classifying products")
        products = classify_products_bulk(products, product_key="product_name")
        print(f"✅ Successfully classified {len(products)} products")

        all_products.extend(products)


    print(f"⏰Inserting products into database")
    insert_data(all_products)
    print(f"✅ Successfully inserted {len(all_products)} products into database")
    
    print(f"⏰Saving products to JSON file")
    save_json(all_products, filename=f"{brand}_products.json")
    print(f"✅ Successfully saved {len(all_products)} products to JSON file")

async def run_all():
    for site in WEBSITES:
        if not site.get("enabled", True):
            continue
        await main(
            BRAND=site["brand"],
            SCHEMA=site["schema"],
            BASE_URL=site["base_url"],
            URLS=site["urls"]
        )

if __name__ == "__main__":
    # asyncio.run(main())
    BRAND = "Shop Simon"
    SCHEMA = shop_simon_schema
    BASE_URL = shop_simon_base_link
    URLS = shop_simon_links[:2]
    asyncio.run(main(BRAND, SCHEMA, BASE_URL, URLS))

