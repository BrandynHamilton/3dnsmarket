import requests
import json
import time
import os
import streamlit as st

opensea_api_key = os.getenv('opensea_api_key')

@st.cache_data()
def fetch_event_type(api_key, event_type, all_events, params, headers):
    base_url = f"https://api.opensea.io/api/v2/events/collection/3dns-powered-domains"
    params['event_type'] = event_type  # Update event_type in params for each call
    
    page_count = 0
    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            fetched_events = data.get("asset_events", [])
            all_events.extend(fetched_events)
            
            page_count += 1
            next_cursor = data.get("next")
            print(f"Fetching {event_type}: Page {page_count}, Events Fetched: {len(fetched_events)}, Total Events: {len(all_events)}, next cursor: {next_cursor}")
            if next_cursor:
                params['next'] = next_cursor
            else:
                break  # Exit loop if there's no next cursor

            time.sleep(1)  # Be mindful of rate limits
        else:
            print(f"Failed to fetch {event_type} data: HTTP {response.status_code}, Response: {response.text}")
            break

@st.cache_data()
def fetch_all_events(api_key, output_file='all_events.json'):
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    params = {
        "limit": 50  # Adjust based on the maximum limit supported by the API
    }

    all_events = []

    # Fetch listings
    fetch_event_type(api_key, "listing", all_events, params.copy(), headers)

    # Fetch sales
    fetch_event_type(api_key, "sale", all_events, params.copy(), headers)

    # Save the fetched events to a JSON file
    with open(output_file, 'w') as file:
        json.dump(all_events, file, indent=4)

    print(f"Total events fetched: {len(all_events)}")
    print(f"Events data saved to '{output_file}'.")

# Replace 'your_api_key_here' with your actual OpenSea API key
fetch_all_events(api_key= opensea_api_key)
