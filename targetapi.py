import requests
import json
import math
import html


def get_raw_data(search_term):

    url = f"https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={search_term}&member_id=20125137631&new_search=true&offset=0&page=%2Fs%2F{search_term.replace(' ', '+')}&platform=mobile&pricing_store_id=2766&store_ids=2766%2C3297%2C2768%2C3264%2C3353&useragent=Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F116.0.0.0+Mobile+Safari%2F537.36&visitor_id=00000000003E01019526BD784284D408&zip=94133"
    # Generate the user-agent string
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    # f = open("target.json", "a")
    # f.write(response.text)
    # f.close()
    return response.json()


def parse_data(data):
    parsed_data = []
    # find product count
    if (
        data.get("data") and
        data["data"].get("search") and
        data["data"]["search"].get("products")
    ):
        itemCount = len(data["data"]["search"]["products"])
        # go through each product and add it to the list
        # temp list that contains a single product and the name and price for it
        for i in range(itemCount):
            product = data["data"]["search"]["products"][i]
            if (product["__typename"] != "ProductSummary"):
                continue
            # check if data is null
            if (
                product.get("item") and
                product.get("price") and
                product["price"].get("formatted_current_price") and
                product["item"].get("enrichment") and
                product["item"]["enrichment"].get("images") and product["item"]["enrichment"].get("buy_url") and
                product["item"]["enrichment"]["images"].get("primary_image_url") and
                product["item"].get("product_description") and
                product["item"]["product_description"].get("title")
            ):
                parsed_data.append({
                    "name": html.unescape(product["item"]["product_description"]["title"]),
                    "price": float(product["price"]["formatted_current_price"][1:]),
                    "unitPrice": "N/A",
                    "unitPriceValue": "N/A",
                    "image": product["item"]["enrichment"]["images"]["primary_image_url"],
                    "minShippingCount": int(math.ceil(50/float(product["price"]["formatted_current_price"][1:]))),
                    "link": product["item"]["enrichment"]["buy_url"],
                    "from": "Target"
                })
    return list({item['name']: item for item in parsed_data}.values())
