"""
Test script for the currency_utils module to verify offline mode functionality.
"""
import unittest
import os
import time
import json
from src.currency_utils import (
    get_exchange_rates,
    get_historical_rates,
    load_from_cache,
    save_to_cache,
    get_cache_file_path
)

class TestOfflineMode(unittest.TestCase):
    """Test suite for offline mode and caching functionality."""
    
    def setUp(self):
        """Create cache directory if it doesn't exist."""
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def test_cache_file_path(self):
        """Test that cache file paths are correctly generated."""
        path = get_cache_file_path('exchange_rates')
        expected_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cache', 'exchange_rates.json')
        self.assertEqual(path, expected_path)
    
    def test_save_and_load_cache(self):
        """Test saving and loading data from cache."""
        test_data = {"USD": 1.0, "EUR": 0.85}
        base_currency = "USD"
        
        # Save to cache
        success = save_to_cache('exchange_rates', test_data, base_currency)
        self.assertTrue(success)
        
        # Load from cache
        cached_data, is_expired = load_from_cache('exchange_rates', base_currency)
        self.assertEqual(cached_data, test_data)
        self.assertFalse(is_expired)  # Should not be expired as we just saved it
    
    def test_exchange_rates_caching(self):
        """Test that exchange rates are properly cached."""
        # First call to get_exchange_rates should either use API or fallback
        rates1, update_time1 = get_exchange_rates("USD")

        # Second call should use cache
        rates2, update_time2 = get_exchange_rates("USD")

        # Rates should be the same
        self.assertEqual(rates1.keys(), rates2.keys())

        # Force refresh should get new data (which might be the same but should have a different timestamp)
        rates3, update_time3 = get_exchange_rates("USD", force_refresh=True)

        # We should have at least some currencies in the response
        self.assertGreater(len(rates1), 0)
        self.assertTrue(all(isinstance(rate, float) for rate in rates1.values()))
    
    def test_historical_rates_caching(self):
        """Test that historical rates are properly cached."""
        # First call to get_historical_rates
        hist_data1 = get_historical_rates("USD", days=7)
        
        # Should have 7 days of data
        self.assertEqual(len(hist_data1), 7)
        
        # Second call should use cache
        hist_data2 = get_historical_rates("USD", days=7)
        
        # Data should be identical
        self.assertEqual(hist_data1.keys(), hist_data2.keys())
        
        # Force refresh should get new data
        hist_data3 = get_historical_rates("USD", days=7, force_refresh=True)
        
        # Should still have 7 days of data
        self.assertEqual(len(hist_data3), 7)

    def test_cache_expiry(self):
        """Test that cache expiry works correctly."""
        # Create a very simple cache file with old timestamp
        cache_file = get_cache_file_path('exchange_rates')
        test_data = {
            "rates": {
                "USD": {
                    "data": {"USD": 1.0, "EUR": 0.85},
                    "timestamp": time.time() - 7200  # 2 hours ago (beyond the 1 hour expiry)
                }
            }
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Load the cache - should be expired
        cached_data, is_expired = load_from_cache('exchange_rates', "USD")
        self.assertTrue(is_expired)

if __name__ == '__main__':
    unittest.main()