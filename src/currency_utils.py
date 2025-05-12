"""
Currency utilities module for Tool-Currency application.
Provides functions for loading, retrieving, and converting currency data.
"""
import json
import os
import requests
from datetime import datetime, timedelta
import time

# Cache variables to store data and avoid repeated API calls/file reads
_currencies_cache = None
_exchange_rates_cache = {}
_historical_rates_cache = {}

# Cache configuration
_cache_expiry = {
    'exchange_rates': 3600,  # Expire current rates after 1 hour
    'historical_rates': 86400  # Expire historical rates after 24 hours
}
_last_updated = {}

def get_cache_file_path(cache_type):
    """
    Get the file path for a specific cache file type.

    Args:
        cache_type (str): Type of cache ('exchange_rates', 'historical_rates')

    Returns:
        str: Absolute path to the cache file
    """
    # Create cache directory if it doesn't exist
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cache')
    if not os.path.exists(cache_dir):
        try:
            os.makedirs(cache_dir)
        except OSError:
            print(f"Warning: Could not create cache directory at {cache_dir}")
            return None

    return os.path.join(cache_dir, f"{cache_type}.json")

def save_to_cache(cache_type, data, base_currency=None):
    """
    Save data to both memory cache and disk cache.

    Args:
        cache_type (str): Type of cache ('exchange_rates', 'historical_rates')
        data (dict): Data to cache
        base_currency (str, optional): Base currency for the rates

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Update in-memory cache
        if cache_type == 'exchange_rates':
            _exchange_rates_cache[base_currency] = data
            _last_updated[f'exchange_rates_{base_currency}'] = time.time()
        elif cache_type == 'historical_rates':
            key = f"{base_currency}_{len(data)}"  # Key format: "USD_30" for 30 days of USD data
            _historical_rates_cache[key] = data
            _last_updated[f'historical_rates_{key}'] = time.time()

        # Get cache file path
        cache_file = get_cache_file_path(cache_type)
        if not cache_file:
            return False

        # Load existing cache file if it exists
        cache_data = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
            except (json.JSONDecodeError, OSError):
                # If file is corrupted, start with empty cache
                cache_data = {}

        # Update cache data
        if cache_type == 'exchange_rates':
            if 'rates' not in cache_data:
                cache_data['rates'] = {}
            cache_data['rates'][base_currency] = {
                'data': data,
                'timestamp': time.time()
            }
        elif cache_type == 'historical_rates':
            if 'rates' not in cache_data:
                cache_data['rates'] = {}
            key = f"{base_currency}_{len(data)}"
            cache_data['rates'][key] = {
                'data': data,
                'timestamp': time.time()
            }

        # Write updated cache to file
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)

        return True
    except Exception as e:
        print(f"Warning: Failed to save to cache: {str(e)}")
        return False

def load_from_cache(cache_type, base_currency=None, days=None):
    """
    Load data from cache (memory or disk).

    Args:
        cache_type (str): Type of cache ('exchange_rates', 'historical_rates')
        base_currency (str, optional): Base currency for the rates
        days (int, optional): Number of days for historical data

    Returns:
        tuple: (data, is_expired) or (None, True) if not found or error
    """
    try:
        # Check in-memory cache first
        if cache_type == 'exchange_rates':
            if base_currency in _exchange_rates_cache:
                # Check if expired
                cache_key = f'exchange_rates_{base_currency}'
                last_update = _last_updated.get(cache_key, 0)
                is_expired = (time.time() - last_update) > _cache_expiry['exchange_rates']
                return _exchange_rates_cache[base_currency], is_expired

        elif cache_type == 'historical_rates' and days:
            key = f"{base_currency}_{days}"
            if key in _historical_rates_cache:
                cache_key = f'historical_rates_{key}'
                last_update = _last_updated.get(cache_key, 0)
                is_expired = (time.time() - last_update) > _cache_expiry['historical_rates']
                return _historical_rates_cache[key], is_expired

        # If not in memory cache, try disk cache
        cache_file = get_cache_file_path(cache_type)
        if not cache_file or not os.path.exists(cache_file):
            return None, True

        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        if 'rates' not in cache_data:
            return None, True

        if cache_type == 'exchange_rates':
            if base_currency in cache_data['rates']:
                data = cache_data['rates'][base_currency]
                timestamp = data.get('timestamp', 0)
                is_expired = (time.time() - timestamp) > _cache_expiry['exchange_rates']

                # Update memory cache
                if not is_expired:
                    _exchange_rates_cache[base_currency] = data['data']
                    _last_updated[f'exchange_rates_{base_currency}'] = timestamp

                return data['data'], is_expired

        elif cache_type == 'historical_rates' and days:
            key = f"{base_currency}_{days}"
            if key in cache_data['rates']:
                data = cache_data['rates'][key]
                timestamp = data.get('timestamp', 0)
                is_expired = (time.time() - timestamp) > _cache_expiry['historical_rates']

                # Update memory cache
                if not is_expired:
                    _historical_rates_cache[key] = data['data']
                    _last_updated[f'historical_rates_{key}'] = timestamp

                return data['data'], is_expired

        # Not found in cache
        return None, True

    except Exception as e:
        print(f"Warning: Failed to load from cache: {str(e)}")
        return None, True

def load_currencies():
    """
    Load currency data from the JSON file.

    Uses a simple memory cache to avoid repeated file reads.

    Returns:
        list: List of currency dictionaries, each containing 'code', 'name', and 'symbol'
    """
    global _currencies_cache

    # Return cached currencies if available
    if _currencies_cache is not None:
        return _currencies_cache

    # Construct file path dynamically for cross-platform compatibility
    currencies_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'currencies.json')

    try:
        with open(currencies_path, 'r', encoding='utf-8') as file:
            # Load and cache the currencies data
            _currencies_cache = json.load(file)['currencies']
            return _currencies_cache
    except FileNotFoundError:
        # Return an empty list if file not found to prevent application crash
        print(f"Warning: Currency data file not found at {currencies_path}")
        return []
    except json.JSONDecodeError:
        # Return an empty list if JSON is invalid to prevent application crash
        print(f"Warning: Invalid JSON in currency data file at {currencies_path}")
        return []

def get_currency_codes():
    """
    Get a list of all available currency codes.
    
    Returns:
        list: List of currency codes (e.g., 'USD', 'EUR', etc.)
    """
    currencies = load_currencies()
    return [currency['code'] for currency in currencies]

def get_currency_name(code):
    """
    Get the full name of a currency based on its code.
    
    Args:
        code (str): The currency code (e.g., 'USD')
        
    Returns:
        str or None: The currency name or None if code not found
    """
    currencies = load_currencies()
    for currency in currencies:
        if currency['code'] == code:
            return currency['name']
    return None

def get_currency_symbol(code):
    """
    Get the symbol of a currency based on its code.
    
    Args:
        code (str): The currency code (e.g., 'USD')
        
    Returns:
        str or None: The currency symbol or None if code not found
    """
    currencies = load_currencies()
    for currency in currencies:
        if currency['code'] == code:
            return currency['symbol']
    return None

def get_exchange_rates(base_currency="USD", force_refresh=False):
    """
    Get current exchange rates for a given base currency.

    Uses three layers of data sources with fallbacks:
    1. Memory cache (fastest)
    2. Disk cache (fast, persists between app restarts)
    3. API call (slowest, requires internet)
    4. Sample data (fallback when all else fails)

    Args:
        base_currency (str): The base currency code (default: 'USD')
        force_refresh (bool): Force refresh from API even if cache is valid

    Returns:
        tuple: (exchange_rates_dict, last_update_time_string)
    """
    # Try to load from cache first, unless force_refresh is True
    if not force_refresh:
        cached_rates, is_expired = load_from_cache('exchange_rates', base_currency)

        # Use cached data if available and not expired
        if cached_rates and not is_expired:
            # Get formatted time string for the cached data
            cache_key = f'exchange_rates_{base_currency}'
            last_update_time = _last_updated.get(cache_key, time.time())
            last_update_str = datetime.fromtimestamp(last_update_time).strftime("%a, %d %b %Y %H:%M:%S +0000")

            return cached_rates, f"{last_update_str} (cached)"

    # If we need to refresh (expired cache or forced refresh), try the API
    try:
        # Check network connectivity first (quick check to Google DNS)
        try:
            requests.get("https://8.8.8.8", timeout=1)
            network_available = True
        except requests.RequestException:
            network_available = False

        if not network_available:
            print("Warning: No network connectivity, using offline data")
            # Use cached data even if expired, or fall back to sample data
            cached_rates, _ = load_from_cache('exchange_rates', base_currency)
            if cached_rates:
                # Get formatted time string for the cached data
                cache_key = f'exchange_rates_{base_currency}'
                last_update_time = _last_updated.get(cache_key, time.time())
                last_update_str = datetime.fromtimestamp(last_update_time).strftime("%a, %d %b %Y %H:%M:%S +0000")

                return cached_rates, f"{last_update_str} (offline mode)"
            else:
                return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000") + " (sample data)"

        # If network is available, try to fetch fresh data
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{base_currency}",
            timeout=5  # 5 second timeout
        )

        # Raise an exception for 4XX and 5XX responses
        response.raise_for_status()

        data = response.json()

        if data.get('result') == 'success':
            # Cache the fresh data
            save_to_cache('exchange_rates', data['rates'], base_currency)
            return data['rates'], data['time_last_update_utc']
        else:
            # API returned failure, try cached data even if expired
            cached_rates, _ = load_from_cache('exchange_rates', base_currency)
            if cached_rates:
                cache_key = f'exchange_rates_{base_currency}'
                last_update_time = _last_updated.get(cache_key, time.time())
                last_update_str = datetime.fromtimestamp(last_update_time).strftime("%a, %d %b %Y %H:%M:%S +0000")

                return cached_rates, f"{last_update_str} (offline mode)"
            else:
                # Fall back to sample data
                return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000") + " (sample data)"

    except (requests.RequestException, json.JSONDecodeError, KeyError) as error:
        # Log the error
        print(f"Error fetching exchange rates: {str(error)}")

        # Try cached data even if expired
        cached_rates, _ = load_from_cache('exchange_rates', base_currency)
        if cached_rates:
            cache_key = f'exchange_rates_{base_currency}'
            last_update_time = _last_updated.get(cache_key, time.time())
            last_update_str = datetime.fromtimestamp(last_update_time).strftime("%a, %d %b %Y %H:%M:%S +0000")

            return cached_rates, f"{last_update_str} (offline mode)"
        else:
            # Fall back to sample data
            return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000") + " (sample data)"

def get_sample_exchange_rates(base_currency="USD"):
    """
    Get sample exchange rates as a fallback when API is unavailable.
    
    Calculates rates for any base currency by normalizing against USD.
    
    Args:
        base_currency (str): The base currency code (default: 'USD')
        
    Returns:
        dict: Exchange rates dictionary with currency codes as keys and rates as values
    """
    # Sample exchange rates (as of May 2025)
    base_rates = {
        "USD": 1.0,
        "EUR": 0.93,
        "GBP": 0.79,
        "JPY": 154.56,
        "CAD": 1.36,
        "AUD": 1.51,
        "CHF": 0.91,
        "CNY": 7.23,
        "INR": 83.34,
        "BRL": 5.04,
        "MXN": 16.62,
        "SGD": 1.34
    }
    
    # If base currency is not USD, recalculate all rates
    if base_currency != "USD":
        # Make sure the base currency exists in our sample data
        if base_currency not in base_rates:
            print(f"Warning: Unknown base currency '{base_currency}', defaulting to USD")
            return base_rates
            
        base_value = base_rates[base_currency]
        converted_rates = {}
        
        # Calculate each rate relative to the new base currency
        for currency, rate in base_rates.items():
            converted_rates[currency] = rate / base_value
            
        return converted_rates
    
    return base_rates

def get_historical_rates(base_currency="USD", days=30, force_refresh=False):
    """
    Get historical exchange rates for a specified number of past days.

    Uses a free API for historical data with fallback to generated sample data.
    Uses disk caching for offline mode and performance.

    Args:
        base_currency (str): The base currency code (default: 'USD')
        days (int): Number of days of historical data to retrieve (default: 30)
        force_refresh (bool): Force refresh from API even if cache is valid

    Returns:
        dict: Dictionary with dates as keys and rate dictionaries as values
    """
    # Try to load from cache first, unless force_refresh is True
    if not force_refresh:
        cached_data, is_expired = load_from_cache('historical_rates', base_currency, days)

        # Use cached data if available and not expired
        if cached_data and not is_expired:
            return cached_data

    # Check if we have network connectivity
    try:
        requests.get("https://8.8.8.8", timeout=1)
        network_available = True
    except requests.RequestException:
        network_available = False

    # If no network or cache is expired but available, use cache anyway
    if not network_available:
        cached_data, _ = load_from_cache('historical_rates', base_currency, days)
        if cached_data:
            return cached_data

    historical_data = {}
    today = datetime.now()
    api_success = False

    # Try to fetch real historical data from API if network is available
    if network_available:
        try:
            # For demonstration, we'll use Open Exchange Rates API
            # In a production app, you would use a paid API with better historical data support
            for i in range(days):
                date = (today - timedelta(days=i)).strftime('%Y-%m-%d')

                # Use a simple rate limiting to avoid API throttling
                if i > 0 and i % 5 == 0:
                    time.sleep(1)

                # Call the API for the specific date
                response = requests.get(
                    f"https://open.er-api.com/v6/historical/{date}?base={base_currency}",
                    timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get('result') == 'success':
                        historical_data[date] = data['rates']
                        api_success = True
                    else:
                        # Use sample data for this date if API call fails
                        historical_data[date] = get_sample_historical_rate(base_currency, i)
                else:
                    # Use sample data for this date if API call fails
                    historical_data[date] = get_sample_historical_rate(base_currency, i)

        except Exception as error:
            print(f"Error fetching historical exchange rates: {str(error)}")
            api_success = False

    # If API calls failed or network unavailable, check for expired cache
    if not api_success or len(historical_data) < days:
        cached_data, _ = load_from_cache('historical_rates', base_currency, days)

        # If we have cached data, use it to fill in any missing dates
        if cached_data:
            # For any missing dates, use cached data
            for date in cached_data:
                if date not in historical_data:
                    historical_data[date] = cached_data[date]

        # If we still don't have enough data, generate sample data
        if len(historical_data) < days:
            for i in range(days):
                date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
                if date not in historical_data:
                    historical_data[date] = get_sample_historical_rate(base_currency, i)

    # Cache the results if we have full data
    if len(historical_data) == days:
        save_to_cache('historical_rates', historical_data, base_currency)

    return historical_data

def get_sample_historical_rate(base_currency="USD", days_ago=0):
    """
    Generate sample historical exchange rates for demo purposes.

    Creates slightly varying rates based on the sample rates to simulate real fluctuations.

    Args:
        base_currency (str): The base currency code
        days_ago (int): Number of days in the past (affects the variation)

    Returns:
        dict: Dictionary of sample historical rates
    """
    import random

    # Get the base sample rates
    base_rates = get_sample_exchange_rates(base_currency)
    historical_rates = {}

    # Add small random variations to each rate
    for currency, rate in base_rates.items():
        # Create a consistent but varying rate using the seed of days_ago
        random.seed(f"{currency}_{days_ago}")

        # Variation factor: between -3% and +3%
        variation = random.uniform(-0.03, 0.03)

        # Calculate the historical rate with variation
        historical_rates[currency] = rate * (1 + variation)

    return historical_rates

def convert_currency(amount, from_currency, to_currency):
    """
    Convert an amount from one currency to another.

    Args:
        amount (float): The amount to convert
        from_currency (str): The source currency code
        to_currency (str): The target currency code

    Returns:
        float or None: The converted amount or None if conversion fails
    """
    # Same currency, no conversion needed
    if from_currency == to_currency:
        return amount

    # Validate input
    if amount < 0:
        print(f"Warning: Negative amount {amount} provided for conversion")
        # Continue with the absolute value
        amount = abs(amount)

    try:
        # Get exchange rates with the from_currency as base
        rates, _ = get_exchange_rates(from_currency)

        # Check if target currency is in the rates
        if to_currency in rates:
            return amount * rates[to_currency]
        else:
            print(f"Warning: Target currency '{to_currency}' not found in exchange rates")
            return None
    except Exception as error:
        # Log any unexpected errors
        print(f"Error during currency conversion: {str(error)}")
        return None