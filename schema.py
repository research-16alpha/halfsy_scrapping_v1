# Define extraction schema (same as before)
farfetch_schema = {
    "name": "Farfetch Products",
    "baseSelector": "li[data-testid='productCard']",
    "fields": [
        {
            "name": "product_link",
            "selector": "a[data-component='ProductCardLink']",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image",
            "selector": "img[data-component='ProductCardImagePrimary']",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "brand_name",
            "selector": "p[data-component='ProductCardBrandName']",
            "type": "text"
        },
        {
            "name": "product_name",
            "selector": "p[data-component='ProductCardDescription']",
            "type": "text"
        },
        {
            "name": "original_price",
            "selector": "p[data-component='PriceOriginal']",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": "p[data-component='PriceFinal']",
            "type": "text"
        },
        {
            "name": "available_sizes",
            "selector": "p[data-component='ProductCardSizesAvailable']",
            "type": "text"
        }
    ]
}

ssense_schema = {
    "name": "SSENSE Products",
    "baseSelector": "div.plp-products__product-tile",
    "fields": [
        {
            "name": "product_link",
            "selector": "a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image",
            "selector": "picture source[media='(min-width: 1025px)']",
            "type": "attribute",
            "attribute": "srcset"
        },
        {
            "name": "brand_name",
            "selector": "span[data-test^='productBrandName']",
            "type": "text"
        },
        {
            "name": "product_name",
            "selector": "span[data-test^='productName']",
            "type": "text"
        },
        {
            "name": "original_price",
            "selector": "span[data-test^='productFormerPrice']",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": "span[data-test^='productCurrentPrice']",
            "type": "text"
        },
        {
            "name": "available_sizes",
            "selector": "",
            "type": "text",
        }
    ]
}

harrods_schema = {
    "name": "Harrods Products",
    "baseSelector": "article[id^='product-']",
    "fields": [
        {
            "name": "product_link",
            "selector": "a[href*='/en-gb/p/']",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image",
            "selector": "picture img",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "brand_name",
            "selector": "p[data-test-id='headline']",
            "type": "text"
        },
        {
            "name": "product_name",
            "selector": "p[data-test-id='product-card-product-name']",
            "type": "text"
        },
        {
            "name": "original_price",
            "selector": "span[data-test-id='initialProductPrice']",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": "span.text-harrods-red",
            "type": "text"
        },
        {
            "name": "available_sizes",
            "selector": "",
            "type": "text",
        }
    ]
}

saks_schema = {
    "name": "Saks Fifth Avenue Products",
    "baseSelector": "div.product-tile",
    "fields": [
        {
            "name": "product_link",
            "selector": "a.thumb-link",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image_link",
            "selector": "picture.tile-image img",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "brand_name",
            "selector": "h2 a.product-brand",
            "type": "text"
        },
        {
            "name": "product_name",
            "selector": "h3.pdp-link a.link",
            "type": "text"
        },
        {
            "name": "price_original",
            "selector": "span.list .formatted_price.bfx-list-price",
            "type": "text"
        },
        {
            "name": "price_final",
            "selector": "span.sales .formatted_sale_price",
            "type": "text"
        },
        {
            "name": "price_range_min",
            "selector": "span.range span.sales .formatted_sale_price:first-of-type",
            "type": "text"
        },
        {
            "name": "price_range_max",
            "selector": "span.range span.sales .formatted_sale_price:last-of-type",
            "type": "text"
        },
        {
            "name": "product_id",
            "selector": "input.tileproduct-detail",
            "type": "attribute",
            "attribute": "data-pid"
        },
        {
            "name": "product_sku",
            "selector": "input.tileproduct-atm-code",
            "type": "attribute",
            "attribute": "data-atm-code"
        },
        {
            "name": "brand_hidden",
            "selector": "input.tileproduct-brandname",
            "type": "attribute",
            "attribute": "data-brandname"
        },
        {
            "name": "color_variants",
            "selector": "a.colorswatch.tile-swatch",
            "type": "attribute_list",
            "attribute": "data-attr-value"
        },
        {
            "name": "color_hex_values",
            "selector": "span.swatch.swatch-circle",
            "type": "attribute_list",
            "attribute": "style"
        },
        {
            "name": "is_on_sale",
            "selector": "span.list.strike-through",
            "type": "exists"
        },
        {
            "name": "add_to_bag_link",
            "selector": "button.ajax-update-atc-button",
            "type": "attribute",
            "attribute": "data-href"
        },
        {
            "name": "wishlist_link",
            "selector": "button.wishlistTile",
            "type": "attribute",
            "attribute": "href"
        }
    ]
}

bloomingdales_schema = {
    "name": "Bloomingdales Products",
    "baseSelector": "li.cell.sortablegrid-product",
    "fields": [
        {
            "name": "product_link",
            "selector": "a[title]",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image",
            "selector": ".picture-container img",
            "type": "attribute",
            "attribute": "data-src"
        },
        {
            "name": "brand_name",
            "selector": ".product-brand",
            "type": "text"
        },
        {
            "name": "product_name",
            "selector": ".product-name",
            "type": "text"
        },
        {
            "name": "original_price",
            "selector": ".price-strike",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": ".show-percent-off .discount",
            "type": "text"
        },
        {
            "name": "available_sizes",
            "selector": "",
            "type": "text",
        }
    ]
}



doverstreetmarket_schema = {
    "name": "Dover Street Market Products",
    "baseSelector": "li[class*='col-span'] article[role='group']",
    "fields": [
        {
            "name": "product_link",
            "selector": "h2 a[href*='/collections/']",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image_link",
            "selector": "img",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "brand_name",
            "selector": "h2 span.block.uppercase",
            "type": "text"
        },
        {
            "name": "product_description",
            "selector": "h2 a",
            "type": "text"
        },
        {
            "name": "product_color",
            "selector": "h2 a span.block:not(.uppercase)",
            "type": "text"
        },
        {
            "name": "price_final",
            "selector": "div[class*='flex'] span:not(.sr-only):not(.line-through)",
            "type": "text"
        },
        {
            "name": "price_original",
            "selector": "span.line-through",
            "type": "text"
        },
        {
            "name": "product_id",
            "selector": "h2[data-id]",
            "type": "attribute",
            "attribute": "data-id"
        }
    ]
}


sample_sale_schema = {
    "name": "260 Sample Sale Products",
    "baseSelector": "div.product-grid__item",
    "fields": [
        {
            "name": "product_link",
            "selector": "a.product-card__name",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image_link",
            "selector": "product-gallery-component img",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "brand_name",
            "selector": "input[name='properties[Vendor]']",
            "type": "attribute",
            "attribute": "value"
        },
        {
            "name": "product_description",
            "selector": "a.product-card__name",
            "type": "text"
        },
        {
            "name": "price_final",
            "selector": "div.product-card__price span.product-card__sale-price",
            "type": "text"
        },
        {
            "name": "price_original",
            "selector": "div.product-card__price span.product-card__compare-price",
            "type": "text"
        },
        {
            "name": "discount_percent",
            "selector": "div.label__percentage",
            "type": "text"
        },
        {
            "name": "availability",
            "selector": "product-card",
            "type": "attribute",
            "attribute": "data-available"
        },
        {
            "name": "stock_level",
            "selector": "stocklevel-component span",
            "type": "text"
        },
        {
            "name": "product_id",
            "selector": "variant-selector option[data-variant-id]",
            "type": "attribute",
            "attribute": "data-variant-id"
        },
        {
            "name": "color_variant",
            "selector": "variant-selector option[data-swatches-option-color]",
            "type": "attribute",
            "attribute": "data-swatches-option-color"
        },
        {
            "name": "size_variant",
            "selector": "variant-selector option[data-swatches-option-size]",
            "type": "attribute",
            "attribute": "data-swatches-option-size"
        }
    ]
}

chicmi_schema = {
    "name": "Chicmi Products",
    "baseSelector": "a.cv2-product-card",
    "fields": [
        {
            "name": "product_link",
            "selector": "a.cv2-product-card",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image",
            "selector": "img.b-lazy, img.b-loaded",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "brand_name",
            "selector": "div.carousel-product-title",
            "type": "text"
        },
        {
            "name": "product_variant",
            "selector": "div.carousel-product-variant",
            "type": "text"
        },
        {
            "name": "price_original",
            "selector": "span.was_price",
            "type": "text"
        },
        {
            "name": "price_final",
            "selector": "span.sale_price",
            "type": "text"
        },
        {
            "name": "discount_percent",
            "selector": "span.discount_percent",
            "type": "text"
        },
        {
            "name": "seller_name",
            "selector": "a.cv2-user-header",
            "type": "text"
        },
        {
            "name": "seller_logo",
            "selector": "a.cv2-user-header img.cv2-user-header-icon",
            "type": "attribute",
            "attribute": "src"
        }
    ]
}

shop_simon_schema = {
    "name": "Shop Simon Products",
    "baseSelector": "div.product-container div.product-item",
    "fields": [
        {
            "name": "product_link",
            "selector": "a.grid-product__link",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "product_image",
            "selector": ".grid-product__image",
            "type": "attribute",
            "attribute": "style"
        },
        {
            "name": "brand_name",
            "selector": ".brandName",
            "type": "text"
        },
        {
            "name": "product_name",
            "selector": ".grid-product__title",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": ".grid-product__price b",
            "type": "text"
        },
        {
            "name": "original_price",
            "selector": ".grid-product__price .grid-product__price--original",
            "type": "text"
        },
        {
            "name": "available_sizes",
            "selector": "",
            "type": "text",
        }
    ]
}