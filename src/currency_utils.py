import json
import os
import requests
from datetime import datetime

# Function to load currency data
def load_currencies():
    currencies_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'currencies.json')
    with open(currencies_path, 'r') as file:
        return json.load(file)['currencies']

# Function to get all currency codes
def get_currency_codes():
    currencies = load_currencies()
    return [currency['code'] for currency in currencies]

# Function to get currency name by code
def get_currency_name(code):
    currencies = load_currencies()
    for currency in currencies:
        if currency['code'] == code:
            return currency['name']
    return None

# Function to get currency symbol by code
def get_currency_symbol(code):
    currencies = load_currencies()
    for currency in currencies:
        if currency['code'] == code:
            return currency['symbol']
    return None

# Sample exchange rates (in a real app, these would come from an API)
def get_exchange_rates(base_currency="USD"):
    # For demo purposes, we'll use a free API for real-time exchange rates
    # Note: In a production app, you'd want to handle API keys more securely
    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{base_currency}")
        data = response.json()
        
        if data.get('result') == 'success':
            return data['rates'], data['time_last_update_utc']
        else:
            # Fallback to sample data if API call fails
            return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    except Exception:
        # Fallback to sample data if API call fails
        return get_sample_exchange_rates(base_currency), datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

# Sample exchange rates as a fallback
def get_sample_exchange_rates(base_currency="USD"):
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
        base_value = base_rates[base_currency]
        converted_rates = {}
        
        for currency, rate in base_rates.items():
            converted_rates[currency] = rate / base_value
            
        return converted_rates
    
    return base_rates

# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
        
    rates, _ = get_exchange_rates(from_currency)
    
    if to_currency in rates:
        return amount * rates[to_currency]
    else:
        # Fallback if rate not found
        return None