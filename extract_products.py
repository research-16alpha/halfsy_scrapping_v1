from optimised_async_scrape import *
from extractor import extract_with_schema, save_json
from schema import farfetch_schema
from links import farfetch_links
from proxies import PROXIES
from base_links import farfetch_base_link

async def main():

    CONCURRENCY_LIMIT = 10
    BRAND_NAME = "Farfetch"
    SCHEMA = farfetch_schema
    BASE_URL = farfetch_base_link
    URLS = farfetch_links

    html_list = await scrape_multiple(urls=URLS, concurrency_limit=CONCURRENCY_LIMIT, proxies = PROXIES)

    all_products = []
    for html in html_list:
        products_results_list = extract_with_schema(html=html, schema = SCHEMA, base_url = BASE_URL)
        all_products.extend(products_results_list)
    save_json(all_products, filename=f"{BRAND_NAME}_products.json")

if __name__ == "__main__":
    asyncio.run(main())    

