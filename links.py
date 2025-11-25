#%%

saks_sale_link = "https://www.saksfifthavenue.com/c/sale-2/sale"
saks_links = []
for page in range(1, 10):
    link = f"{saks_sale_link}?start={page * 96}&sz=24"
    saks_links.append(link)


farfetch_sale_link = "https://www.farfetch.com/in/shopping/men/sale/all/items.aspx"
farfetch_links = []
for page in range(1, 30):
    link = f"{farfetch_sale_link}?page={page}"
    farfetch_links.append(link)


ssense_sale_link = "https://www.ssense.com/en-in/women/sale"
ssense_links = []
for page in range(1, 30):
    link = f"{ssense_sale_link}?page={page}"
    ssense_links.append(link)

harrods_sale_links = "https://www.harrods.com/en-gb/sale"
harrods_links = []
for page in range(1, 30):
    link = f"{harrods_sale_links}?page={page}"
    harrods_links.append(link)

doversstreet_sale_link = "https://shop.doverstreetmarket.com/collections/all-mens"
doversstreet_links = []
for page in range(1, 30):
    link = f"{doversstreet_sale_link}?page={page}"
    doversstreet_links.append(link)

bloomingdales_sale_link = f"https://www.bloomingdales.com/shop/sale/men"
bloomingdales_suffix = "?id=1001174"
bloomingdales_links = []
for page in range(1, 30):
    link = f"{bloomingdales_sale_link}/Pageindex/{page}{bloomingdales_suffix}"
    bloomingdales_links.append(link)

shop_simon_link = "https://shop.simon.com/collections/store-adidas?cid=DLP%3APC2%3AAdidas%3AExtra50"
shop_simon_links = []
for page in range(1, 10):
    link = f"{shop_simon_link}&page={page}"
    shop_simon_links.append(link)