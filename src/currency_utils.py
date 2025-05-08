"""
Currency utilities module for Tool-Currency application.
Provides functions for loading, retrieving, and converting currency data.
"""
import json
import os
import requests
from datetime import datetime

# Cache variable to store currencies to avoid repeated file reads
_currencies_cache = None

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

def get_exchange_rates(base_currency="USD"):
    """
    Get current exchange rates for a given base currency.
    
    Attempts to fetch real-time rates from an API, with fallback to sample data.
    
    Args:
        base_currency (str): The base currency code (default: 'USD')
        
    Returns:
        tuple: (exchange_rates_dict, last_update_time_string)
    """
    # For demo purposes, we use a free API for real-time exchange rates
    # In a production app, you'd want to handle API keys more securely
    try:
        # Use a timeout to avoid hanging if the API is slow to respond
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{base_currency}",
            timeout=5  # 5 second timeout
        )
        
        # Raise an exception for 4XX and 5XX responses
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('result') == 'success':
            return data['rates'], data['time_last_update_utc']
        else:
            # Fallback to sample data if API response isn't successful
            return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    except (requests.RequestException, json.JSONDecodeError, KeyError) as error:
        # Log the error (in a real app, use a proper logging system)
        print(f"Error fetching exchange rates: {str(error)}")
        # Fallback to sample data if API call fails for any reason
        return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

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