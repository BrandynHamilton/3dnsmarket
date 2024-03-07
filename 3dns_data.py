from flask import Flask, jsonify, request, abort
import json
import os
from functools import wraps
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        API_KEY = os.getenv('API_KEY') 
        # Now checking for the API key in the query string instead of the headers
        received_key = request.args.get('api_key', '')
        print(f"Received API Key: {received_key}")
        print(f"Expected API Key: {API_KEY}")
        if not received_key: 
            abort(401)  # Unauthorized access
        return f(*args, **kwargs)
    return decorated_function

@app.route('/listings')
@require_api_key
def get_listings():
    try:
        with open('listings.json', 'r') as f:
            listings = json.load(f)
        return jsonify(listings)
    except FileNotFoundError:
        return jsonify({"error": "Listings file not found."}), 404

@app.route('/descriptions')
@require_api_key
def get_descriptions():
    try:
        with open('all_descriptions.json', 'r') as f:
            descriptions = json.load(f)
        return jsonify(descriptions)
    except FileNotFoundError:
        return jsonify({"error": "Descriptions file not found."}), 404

@app.route('/events')
@require_api_key
def get_events():
    try:
        with open('all_events.json', 'r') as f:
            events = json.load(f)
        return jsonify(events)
    except FileNotFoundError:
        return jsonify({"error": "Events file not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
