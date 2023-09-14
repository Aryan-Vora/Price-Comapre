import requests
import json
import math


def get_raw_data(search):
    apisearch = search.replace(" ", "%20")
    headersearch = search.replace(" ", "+")
    url = "https://www.walmart.com/orchestra/snb/graphql/Search/48093560def448db9dad9bcfc8e5b556413f9bd4252bc7a300e26df3a24596b3/search?variables=%7B%22id%22%3A%22%22%2C%22affinityOverride%22%3A%22store_led%22%2C%22dealsId%22%3A%22%22%2C%22query%22%3A%22"+apisearch+"%22%2C%22page%22%3A1%2C%22prg%22%3A%22mWeb%22%2C%22catId%22%3A%22%22%2C%22facet%22%3A%22%22%2C%22sort%22%3A%22best_match%22%2C%22rawFacet%22%3A%22%22%2C%22seoPath%22%3A%22%22%2C%22ps%22%3A40%2C%22limit%22%3A40%2C%22ptss%22%3A%22%22%2C%22trsp%22%3A%22%22%2C%22beShelfId%22%3A%22%22%2C%22recall_set%22%3A%22%22%2C%22module_search%22%3A%22%22%2C%22min_price%22%3A%22%22%2C%22max_price%22%3A%22%22%2C%22storeSlotBooked%22%3A%22%22%2C%22additionalQueryParams%22%3A%7B%22hidden_facet%22%3Anull%2C%22translation%22%3Anull%2C%22isMoreOptionsTileEnabled%22%3Atrue%7D%2C%22searchArgs%22%3A%7B%22query%22%3A%22"+apisearch+"%22%2C%22cat_id%22%3A%22%22%2C%22prg%22%3A%22mWeb%22%2C%22facet%22%3A%22%22%7D%2C%22fitmentFieldParams%22%3A%7B%22powerSportEnabled%22%3Atrue%2C%22dynamicFitmentEnabled%22%3Afalse%2C%22extendedAttributesEnabled%22%3Afalse%7D%2C%22fitmentSearchParams%22%3A%7B%22id%22%3A%22%22%2C%22affinityOverride%22%3A%22store_led%22%2C%22dealsId%22%3A%22%22%2C%22query%22%3A%22" + \
        apisearch+"%22%2C%22page%22%3A1%2C%22prg%22%3A%22mWeb%22%2C%22catId%22%3A%22%22%2C%22facet%22%3A%22%22%2C%22sort%22%3A%22best_match%22%2C%22rawFacet%22%3A%22%22%2C%22seoPath%22%3A%22%22%2C%22ps%22%3A40%2C%22limit%22%3A40%2C%22ptss%22%3A%22%22%2C%22trsp%22%3A%22%22%2C%22beShelfId%22%3A%22%22%2C%22recall_set%22%3A%22%22%2C%22module_search%22%3A%22%22%2C%22min_price%22%3A%22%22%2C%22max_price%22%3A%22%22%2C%22storeSlotBooked%22%3A%22%22%2C%22additionalQueryParams%22%3A%7B%22hidden_facet%22%3Anull%2C%22translation%22%3Anull%2C%22isMoreOptionsTileEnabled%22%3Atrue%7D%2C%22searchArgs%22%3A%7B%22query%22%3A%22" + \
        apisearch+"%22%2C%22cat_id%22%3A%22%22%2C%22prg%22%3A%22mWeb%22%2C%22facet%22%3A%22%22%7D%2C%22cat_id%22%3A%22%22%2C%22_be_shelf_id%22%3A%22%22%7D%2C%22enableFashionTopNav%22%3Afalse%2C%22enableRelatedSearches%22%3Atrue%2C%22enablePortableFacets%22%3Atrue%2C%22enableFacetCount%22%3Atrue%2C%22fetchMarquee%22%3Atrue%2C%22fetchSkyline%22%3Atrue%2C%22fetchGallery%22%3Afalse%2C%22fetchSbaTop%22%3Atrue%2C%22fetchDac%22%3Afalse%2C%22tenant%22%3A%22WM_GLASS%22%2C%22enableFlattenedFitment%22%3Atrue%2C%22enableMultiSave%22%3Afalse%2C%22pageType%22%3A%22SearchPage%22%7D"

    payload = {}
    headers = {
        'authority': 'www.walmart.com',
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/json',
        'referer': 'https://www.walmart.com/search?q=' + headersearch + '&affinityOverride=store_led',
        'sec-ch-ua-mobile': '?1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'wm_mp': 'true',
        'wm_page_url': 'https://www.walmart.com/search?q=' + headersearch + '&affinityOverride=store_led',
        'x-apollo-operation-name': 'Search',
        'x-enable-server-timing': '1',
        'x-latency-trace': '1',
        'x-o-bu': 'WALMART-US',
        'x-o-ccm': 'server',
        'x-o-correlation-id': '2MS5v6UfN0rmM555DOCT1Tr80w4kNwWcY2zC',
        'x-o-gql-query': 'query Search',
        'x-o-mart': 'B2C',
        'x-o-platform': 'rweb',
        'x-o-platform-version': 'main-1.95.1-c3c307-0823T0610',
        'x-o-segment': 'oaoh'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def parse_data(data):
    parsed_data = []
    # find product count
    if (
        data.get("data") and
        data["data"].get("search") and
        data["data"]["search"].get("searchResult") and
        data["data"]["search"]["searchResult"].get("itemStacks") and
        data["data"]["search"]["searchResult"]["itemStacks"][0] and
        data["data"]["search"]["searchResult"]["itemStacks"][0].get("itemsV2")
    ):
        itemCount = len(data["data"]["search"]["searchResult"]
                        ["itemStacks"][0]["itemsV2"])

        # go through each product and add it to the list
        # temp list that contains a single product and the name and price for it
        for i in range(itemCount):
            product = data["data"]["search"]["searchResult"]["itemStacks"][0]["itemsV2"][i]
            if (product["__typename"] != "Product"):
                continue
            # check if price or name is null
            if (
                product.get("name") and
                product.get("priceInfo") and
                product["priceInfo"].get("currentPrice") and
                product["priceInfo"]["currentPrice"].get("price") and
                product["priceInfo"].get("unitPrice") and
                product["priceInfo"]["unitPrice"].get("priceString") and
                product["priceInfo"]["unitPrice"].get("price") and
                product.get("imageInfo") and
                product["imageInfo"].get("thumbnailUrl")
            ):
                parsed_data.append({
                    "name": product["name"],
                    "price": product["priceInfo"]["currentPrice"]["price"],
                    "unitPrice": product["priceInfo"]["unitPrice"]["priceString"],
                    "unitPriceValue": product["priceInfo"]["unitPrice"]["price"],
                    "image": product["imageInfo"]["thumbnailUrl"],
                    "minShippingCount": int(math.ceil(50/product["priceInfo"]["currentPrice"]["price"])),
                    "link": "https://walmart.com"+product["canonicalUrl"],
                    "from": "Walmart"

                })
    return list({item['name']: item for item in parsed_data}.values())
