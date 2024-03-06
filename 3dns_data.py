from flask import Flask, jsonify
import requests

app = Flask(__name__)

def fetch_offers():
    url = "https://api.opensea.io/api/v2/offers/collection/3dns-powered-domains/all"
    headers = {
        "accept": "application/json",
        "x-api-key": "95487450cabd40c880636b6ddefcc807"  # Replace with your actual API key
    }
    params = {
        "limit": 100
    }

    offers = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        offers.extend(data.get("offers", []))
        
        next_cursor = data.get("next", None)
        if not next_cursor:
            break
        params["cursor"] = next_cursor  # Update the cursor for the next page

    return offers

@app.route('/offers', methods=['GET'])
def get_offers():
    offers = fetch_offers()  # Fetch offers each time the endpoint is accessed
    return jsonify(offers)

if __name__ == '__main__':
    app.run(debug=True)
