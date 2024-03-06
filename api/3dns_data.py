from flask import Flask, jsonify, json

app = Flask(__name__)

@app.route('/api/listings', methods=['GET'])
def get_listings():
    with open('../listings.json', 'r') as f:
        listings = json.load(f)
    return jsonify(listings)
