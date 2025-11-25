from schema import *
from links import *
from base_links import *

WEBSITES = [
    {
        "brand": "Bloomingdales",
        "schema": bloomingdales_schema,
        "base_url": bloomingdales_base_link,
        "urls": bloomingdales_links[:1]
    },
    {
        "brand": "Farfetch",
        "schema": farfetch_schema,
        "base_url": farfetch_base_link,
        "urls": farfetch_links
    },
    {
        "brand": "Ssense",
        "schema": ssense_schema,
        "base_url": ssense_base_link,
        "urls": ssense_links
    },
    {
        "brand": "Harrods",
        "schema": harrods_schema,
        "base_url": harrods_base_link,
        "urls": harrods_links
    },
    {
      "brand": "Shop Simon",
      "schema": shop_simon_schema,
      "base_url": shop_simon_base_link,
      "urls": shop_simon_links  
    }
]