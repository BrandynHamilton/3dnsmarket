import requests
import json
import time
from flipside import Flipside
import os
import streamlit as st

opensea_api_key = os.getenv('opensea_api_key')

@st.cache_data(ttl=86400)
def fetch_listings(api_key, delay_between_requests=1):
    base_url = "https://api.opensea.io/api/v2/listings/collection/3dns-powered-domains/all"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    params = {"limit": 100} 

    listings = []
    page_count = 0

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            fetched_listings = data.get("listings", [])
            listings.extend(fetched_listings)
            page_count += 1
            
            # Extract and print the cursor
            next_cursor = data.get("next")
            print(f"Page {page_count}, Cursor: {next_cursor}, Listings Fetched: {len(fetched_listings)}")
            
            if next_cursor:
                params['next'] = next_cursor  # Update the 'next' parameter for the next request
            else:
                break  # No more pages to fetch
                
            # Implementing delay
            time.sleep(delay_between_requests)
            
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break

    print(f"Total pages fetched: {page_count}")
    print(f"Total listings fetched: {len(listings)}")
    
    # Save the fetched listings to a file
    with open('listings.json', 'w') as f:
        json.dump(listings, f)

fetch_listings(api_key= opensea_api_key, delay_between_requests=1)

@st.cache_data(ttl=86400)
def fetch_all_descriptions(api_key, descriptions_file='all_descriptions.json', delay_between_requests=1):
    base_url = "https://api.opensea.io/api/v2/collection/3dns-powered-domains/nfts"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    params = {"limit": 100}

    all_descriptions = []

    page_count = 0
    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            fetched_descriptions = data.get("nfts", [])
            
            # Process only name and identifier for each description
            for description in fetched_descriptions:
                processed_description = {
                    "name": description.get('name'),
                    "identifier": description.get('identifier')
                }
                all_descriptions.append(processed_description)
            
            page_count += 1
            next_cursor = data.get("next")
            print(f"Page {page_count}, Cursor: {next_cursor} Descriptions Fetched: {len(fetched_descriptions)}, total fetched: {len(all_descriptions)}")
            
            
            if next_cursor:
                params['next'] = next_cursor
            else:
                break  # No more pages to fetch

            time.sleep(delay_between_requests)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break

    print(f"Total pages fetched: {page_count}, Total descriptions fetched: {len(all_descriptions)}")
    
    # Save the processed descriptions to a file
    with open(descriptions_file, 'w') as f:
        json.dump(all_descriptions, f)

fetch_all_descriptions(api_key= opensea_api_key)


