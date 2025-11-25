#%%

from google import genai
import os
from dotenv import load_dotenv
import json
from google.genai import types
from pydantic import BaseModel
from typing import Dict, List, Optional


# Pydantic Model
class ProductClassification(BaseModel):
    category: str
    sub_category: str
    gender: str


class ProductClassificationBatchItem(BaseModel):
    index: int
    category: str
    sub_category: str
    gender: str


class ProductClassificationBatchResponse(BaseModel):
    items: List[ProductClassificationBatchItem]


# Load ENV variables & initialize client once
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def classify_product(product_name: str) -> dict:
    """
    Takes in a product description string and returns
    the classification JSON (category, sub-category, gender)
    """

    prompt = _single_prompt(product_name)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProductClassification,
        ),
    )

    return response.parsed.model_dump()


def classify_products_bulk(
    products: List[Dict],
    product_key: str = "product_name"
) -> List[Dict]:
    """
    Accepts a list of product dicts, classifies them in a single Gemini call,
    and returns the list with category/sub_category/gender fields injected.
    """

    if not products:
        return []

    payload = []
    index_map = {}

    for idx, product in enumerate(products):
        description = product[product_key]
        if not description:
            continue
        payload.append({"index": idx, "description": description})
        index_map[idx] = product

    if not payload:
        return products

    prompt = _batch_prompt(payload)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProductClassificationBatchResponse,
        ),
    )

    parsed = response.parsed
    if not parsed or not parsed.items:
        return products

    for item in parsed.items:
        target = index_map.get(item.index)
        if not target:
            continue
        target["product_category"] = item.category
        target["product_sub_category"] = item.sub_category
        target["product_gender"] = item.gender

    return products


def _single_prompt(product_name: str) -> str:
    return f"""
    You are a product classifier.

    Given the product description below, classify:

    1. category (e.g., shirt, jeans, shoes, watch, saree, kurta, hoodie, etc.)
    2. sub_category (e.g., casual, formal, sport, etc.)
    3. gender (men, women, unisex, kids)

    If you are not sure about the category or sub-category, return "unknown".
    If you are not sure about the gender, return "unknown".

    Return ONLY valid JSON. No extra text.

    Product Description: "{product_name}"

    JSON FORMAT:
    {{
      "category": "",
      "sub_category": "",
      "gender": ""
    }}
    """


def _batch_prompt(payload: List[Dict]) -> str:
    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)
    return f"""
    You are a product classifier.

    You will receive a list of objects, each containing an "index" and a "description".
    For each entry, classify:
      1. category (e.g., shirt, jeans, shoes, watch, saree, kurta, hoodie, etc.)
      2. sub_category (e.g., casual, formal, sport, etc.)
      3. gender (men, women, unisex, kids)

    If unsure about a field, return "unknown".

    Return ONLY valid JSON that matches this schema:
    {{
      "items": [
        {{
          "index": 0,
          "category": "",
          "sub_category": "",
          "gender": ""
        }}
      ]
    }}

    Data:
    {payload_json}
    """


if __name__ == "__main__":
    products = json.load(open("DoversStreet_products.json"))
    firstProduct = products[0]
    productName = firstProduct["product_description"]
    response = classify_product(productName)

    products = products[:10]
    products = classify_products_bulk(products, product_key="product_description")


