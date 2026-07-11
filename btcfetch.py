"""
btc_price.py

Fetches the current Bitcoin (BTC) price in USD using the CoinGecko API
and prints it to the console.

Note: CoinGecko's free public API has a fairly strict rate limit
(roughly 10-30 calls per minute depending on load). If you run this
script too many times in quick succession, you may see a
"429 Too Many Requests" error - if so, just wait a minute before
trying again.
"""

import requests

# CoinGecko's "simple price" endpoint lets us request the price of one
# or more coins in one or more currencies without needing an API key.
API_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_btc_price():
    """
    Fetch the current BTC price in USD from CoinGecko.

    Returns:
        float: The current BTC price in USD, or None if the request failed.
    """
    params = {
        "ids": "bitcoin",       # coin we want the price for
        "vs_currencies": "usd"  # currency to price it in
    }

    # Some servers (including CoinGecko at times) reject requests that don't
    # include a User-Agent header, treating them as bot/script traffic.
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BTC-Price-Script/1.0)"
    }

    try:
        # Make the GET request with a timeout so the script doesn't hang forever
        response = requests.get(API_URL, params=params, headers=headers, timeout=10)

        # Handle rate limiting specifically, since it's the most common
        # issue with CoinGecko's free tier and has a clear fix (wait).
        if response.status_code == 429:
            print("Error: Rate limit exceeded (429). CoinGecko's free API only "
                  "allows a limited number of requests per minute. Please wait "
                  "about a minute and try again.")
            return None

        # Raise an exception if the HTTP status code indicates an error (4xx/5xx)
        response.raise_for_status()

        # Parse the JSON response body
        data = response.json()

        # Expected shape: {"bitcoin": {"usd": 12345.67}}
        price = data["bitcoin"]["usd"]
        return price

    except requests.exceptions.Timeout:
        print("Error: The request to CoinGecko timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to CoinGecko. Check your internet connection.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error: HTTP error occurred - {http_err}")
    except (KeyError, ValueError):
        print("Error: Unexpected response format from CoinGecko API.")
    except requests.exceptions.RequestException as err:
        print(f"Error: An unexpected error occurred - {err}")

    return None


def main():
    price = get_btc_price()

    if price is not None:
        print(f"Current Bitcoin price: ${price:,.2f} USD")
    else:
        print("Failed to fetch Bitcoin price.")


if __name__ == "__main__":
    main()
