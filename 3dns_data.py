from flask import Flask, jsonify
import requests

app = Flask(__name__)

def fetch_listings():
    url = "https://api.opensea.io/api/v2/listings/collection/3dns-powered-domains/all"
    headers = {
        "accept": "application/json",
        "x-api-key": "95487450cabd40c880636b6ddefcc807"  # Replace with your actual API key
    }
    params = {
        "limit": 100
    }

    listings = []
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        listings.extend(data.get("listings", []))
        
        next_cursor = data.get("next", None)
        if not next_cursor:
            break
        params["cursor"] = next_cursor  # Update the cursor for the next page

    return listings

@app.route('/listings', methods=['GET'])
def get_listings():
    listings = fetch_listings()  # Fetch offers each time the endpoint is accessed
    return jsonify(listings)

if __name__ == '__main__':
    app.run(debug=True)
