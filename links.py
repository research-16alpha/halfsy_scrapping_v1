#%%

saks_base_link = "https://www.saksfifthavenue.com/c/sale-2/sale"
saks_links = []
for page in range(1, 10):
    link = f"{saks_base_link}?start={page * 96}&sz=24"
    print(link)
    saks_links.append(f"{saks_base_link}?start={page * 96}&sz=24")


farfetch_base_link = "https://www.farfetch.com/in/shopping/men/sale/all/items.aspx"
farfetch_links = []
for page in range(1, 30):
    link = f"{farfetch_base_link}?page={page}"
    print(link)
    farfetch_links.append(f"{farfetch_base_link}?page={page}")