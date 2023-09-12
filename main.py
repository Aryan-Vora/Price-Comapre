from itertools import groupby
from operator import itemgetter
import walmartapi
import json
import targetapi
from itertools import groupby
from operator import itemgetter
product_names = [
    "Hand sanitizer",
    "Hand soap",
    "Cleaning wipes",
    "Faical tissues",
    "Kitchen towels",
    "Toilet papers",
    "Trash bags",
    "Dish soap",
    "Sponges",
    "Multi-surface spray",
    "Colgate toothpaste",
    "Oral-B toothbrush",
    "Oral-B floss",
    "Listerine mouthwash",
    "Head & Shoulders shampoo",
    "Pantene conditioner",
    "Dove body wash",
    "Secret deodorant",
    "Neutrogena sunscreen",
    "CeraVe facial cleanser",
    "CeraVe moisturizer",
    "Eucerin Original Healing Hand Cream",
    "Aquaphor Lip Repair",
    "Tresemme hair styling gel",
    "Gillette razors",
    "Gillette shaving cream",
    "TRESemmé Extra Hold Hairspray",
    "Neutrogena Sunscreen",
    "Always Infinity FlexFoam Overnight Pads",
    "Tampax Pearl Ultra Tampons",
    "Poise Sensitive Skin Pantyliners",
    "Summer's Eve Cleansing Cloths",
    "DivaCup menstrual cup",
    "Notebooks",
    "Pens",
    "Sharpie markers",
    "Highlighters",
    "Post-it notes",
    "Binders",
    "Oreo Cookies",
    "Cheetos",
    "Doritos",
    "Lays Chips",
    "Pringles Chips",
    "Kettle Potato Chips",
    "Snyder's Pretzels",
    "Goldfish",
    "Twix",
    "TitKat",
    "Reese's Peanut Butter Cups",
    "Snickers",
    "Skinny Pop Popcorn",
    "Pop Secret Microwave Popcorn",
    "Smartfood White Cheddar Popcorn",
    "Kettle Brand Microwave Popcorn",
    "Trail mix",
    "Clif Bars",
    "Fruit snacks",
    "KIND Chocolate & Nuts Bars",
    "Gatorade",
    "Red Bull",
    "Pepsi",
    "Diet Coke",
    "Sprite",
    "Ginger Ale",
    "Cranberry Juice",
    "Orange Juice",
    "Simply Lemonade",
    "V8 Vegetable Juice",
    "Starbucks Coffee",
    "LaCroix sparkling water",
    "Yerba Mate",
    "GT's Kombucha",
    "Kevita Kombucha",
    "Cheerios",
    "Cinnamon Toast Crunch Cereal",
    "Cup Noodles",
    "Instant Noodles",
    "First-Aid kit",
    "Tylenol Extra Strength pain relievers",
    "Thermacare Heatwraps heat pads",
    "Eye drops",
    "Zyrtec Allergy Tablets",
    "Tums Stomachache Tablets",
    "Dramamine Motion Sickness Tablets",
    "Balloons",
    "Confetti",
    "Streamers",
    "Party Hats",
    "Noisemakers",
    "Solo Cups",
    "Birthday Candles",
    "Water bottle",
    "Flash drive",
    "Hangers",
    "Stuffed animal"
]


def check_availability(product_names):  # will get rate limited if we do this

    for name in product_names:
        walmartapi.get_raw_data(name)
        print("Walmart: " + name)
        targetapi.get_raw_data(name)
        print("Target: " + name)


def get_json_search(user_input):
    items = sorted((walmartapi.parse_data(walmartapi.get_raw_data(user_input)) +
                    targetapi.parse_data(targetapi.get_raw_data(user_input))), key=lambda x: x["price"])
    f = open("items.json", "w")
    f.write(json.dumps(items))
    f.close()


def test_advanced_search(name):
    # Load data from the JSON file
    with open(name, "r") as file:
        data = json.load(file)

    def custom_sort(item):
        return int(item["price"]), item["name"]

    sorted_data = sorted(data, key=custom_sort)

    previous_from = None
    for item in sorted_data:
        if item["from"] != previous_from:
            print(f"From: {item['from']}")
        print(f"  Name: {item['name']}, Price: {item['price']}")
        previous_from = item["from"]


def advanced_search(data):
    data.sort(key=itemgetter('price'))
    price_groups = {}
    for entry in data:
        rounded_price = round(entry['price'])
        if rounded_price in price_groups:
            price_groups[rounded_price].append(entry)
        else:
            price_groups[rounded_price] = [entry]

    # Sort within each price group by name
    for price in price_groups:
        price_groups[price].sort(key=itemgetter('name'))

    # Ensure 'from' values are different within each price and name sorted group
    for price in price_groups:
        from_count = {}
        unique_entries = []
        for entry in price_groups[price]:
            if entry['from'] in from_count:
                from_count[entry['from']] += 1
                entry['from'] = f"{entry['from']} ({from_count[entry['from']]})"
            else:
                from_count[entry['from']] = 1

            unique_entries.append(entry)

        # Remove duplicates based on 'name' and 'from'
        seen_entries = set()
        price_groups[price] = []
        for entry in unique_entries:
            entry_key = (entry['name'], entry['from'])
            if entry_key not in seen_entries:
                seen_entries.add(entry_key)
                price_groups[price].append(entry)

    # Create a list of dictionaries for the final data
    final_data = []
    for price in price_groups:
        for entry in price_groups[price]:
            final_data.append(entry)
    return final_data
