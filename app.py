from flask import Flask, request, render_template, session
from flask_session import Session
import targetapi
import walmartapi
import main
from flask import jsonify

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session["user_input"] = request.form.get('userInput')
        session["items"] = sorted((walmartapi.parse_data(
            walmartapi.get_raw_data(session["user_input"]))+targetapi.parse_data(targetapi.get_raw_data(session["user_input"]))), key=lambda x: x["price"])
        session["sort_by"] = 'price'
        return render_template('index.html', user_input=session["user_input"], items=session["items"], itemCount=len(session["items"]))
    return render_template('index.html', user_input='', matching_items=[], itemCount=0)


@app.route('/sort', methods=['POST'])
def sort_items():
    sort_option = request.form['sort-by']
    items = session["items"]
    if sort_option == 'price':
        items.sort(key=lambda x: x['price'])
        session["sort_by"] = 'Price'
    elif sort_option == 'name':
        items.sort(key=lambda x: x['name'])
        session["sort_by"] = 'Name'
    elif sort_option == 'walmart':
        items = [item for item in items if item['from'] == 'Walmart']
        items.sort(key=lambda x: x['price'])
        session["sort_by"] = 'Walmart'
    elif sort_option == 'target':
        items = [item for item in items if item['from'] == 'Target']
        items.sort(key=lambda x: x['price'])
        session["sort_by"] = 'Target'
    elif sort_option == 'advanced':
        items = main.advanced_search(session["items"])
        session["sort_by"] = 'Advanced'

    return render_template('index.html', user_input=session["user_input"], items=items, itemCount=len(items), selected_option=session["sort_by"])


@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        try:
            user_input = request.headers.get('name')
            retailer = request.headers.get('retailer')
            max_price_header = request.headers.get('max-price')

            if retailer is not None:
                retailer = retailer.lower()

            # Check if user_input is empty
            if not user_input:
                return jsonify(error='Name header is missing or empty'), 400

            walmart_data = None
            target_data = None

            # Check the value of the 'retailer' header
            if retailer == 'walmart':
                walmart_data = walmartapi.get_raw_data(user_input)
            elif retailer == 'target':
                target_data = targetapi.get_raw_data(user_input)
            else:
                # If 'retailer' is neither 'walmart' nor 'target', get data from both
                walmart_data = walmartapi.get_raw_data(user_input)
                target_data = targetapi.get_raw_data(user_input)

            # Check if the API calls were successful
            if (walmart_data is None and retailer == 'walmart') or (target_data is None and retailer == 'target'):
                return jsonify(error='Failed to retrieve data from the specified retailer'), 500

            walmart_items = None
            target_items = None

            # Parse data based on retailer
            if retailer == 'walmart':
                walmart_items = walmartapi.parse_data(walmart_data)
            elif retailer == 'target':
                target_items = targetapi.parse_data(target_data)
            else:
                walmart_items = walmartapi.parse_data(walmart_data)
                target_items = targetapi.parse_data(target_data)

            # Check if the parsing of data was successful
            if (walmart_items is None and retailer == 'walmart') or (target_items is None and retailer == 'target'):
                return jsonify(error='Failed to parse data from the specified distributor'), 500

            # Combine and sort the items
            items = sorted((walmart_items or []) +
                           (target_items or []), key=lambda x: x["price"])

            # Filter items based on max-price header
            if max_price_header is not None:
                try:
                    max_price = float(max_price_header)
                    items = [item for item in items if item.get(
                        "price", 0) <= max_price]
                except ValueError:
                    return jsonify(error='max-price must be a number'), 400

            return jsonify(items=items)

        except Exception as e:
            return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
