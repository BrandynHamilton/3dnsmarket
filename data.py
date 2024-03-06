import requests
import json
import time

def fetch_listings(api_key, delay_between_requests=1):
    base_url = "https://api.opensea.io/api/v2/listings/collection/3dns-powered-domains/all"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    params = {"limit": 100}  # Start with the first page of 100 listings

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
    
    # Optionally, save the fetched listings to a file
    with open('listings.json', 'w') as f:
        json.dump(listings, f)

# Replace 'your_api_key' with your actual OpenSea API key
fetch_listings(api_key='c0c9ef9df89042059cee12e5ca9197e9', delay_between_requests=1)
