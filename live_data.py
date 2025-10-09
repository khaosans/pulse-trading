"""
Live Market Data Module with Rate Limiting & Caching
Uses yfinance (free, no API key required) with smart fallbacks
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from functools import lru_cache
import time

class LiveMarketData:
    """
    Manages live market data with:
    - Rate limiting to prevent throttling
    - Caching to reduce API calls
    - Automatic fallback to synthetic data
    - Error handling for robustness
    """
    
    def __init__(self):
        self.last_api_call = {}
        self.min_interval = 60  # Minimum 60 seconds between API calls per symbol
        self.cache = {}
        self.cache_duration = 300  # Cache for 5 minutes
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_live_price(_self, symbol):
        """
        Get live price with rate limiting and caching
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Current price data or None if failed
        """
        try:
            # Rate limiting check
            current_time = time.time()
            if symbol in _self.last_api_call:
                time_since_last = current_time - _self.last_api_call[symbol]
                if time_since_last < _self.min_interval:
                    # Return cached data if available
                    if symbol in _self.cache:
                        return _self.cache[symbol]
                    return None
            
            # Fetch live data
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant data
            live_data = {
                'symbol': symbol,
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'change': info.get('regularMarketChange', 0),
                'change_pct': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'open': info.get('regularMarketOpen', 0),
                'prev_close': info.get('previousClose', 0)
            }
            
            # Update tracking
            _self.last_api_call[symbol] = current_time
            _self.cache[symbol] = live_data
            
            return live_data
            
        except Exception as e:
            print(f"Error fetching live data for {symbol}: {e}")
            # Return cached data if available
            if symbol in _self.cache:
                return _self.cache[symbol]
            return None
    
    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_historical_data(_self, symbol, period='1mo', interval='1d'):
        """
        Get historical price data with caching
        
        Args:
            symbol: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            DataFrame: Historical price data
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                return None
                
            # Rename columns to match our format
            hist = hist.reset_index()
            hist.columns = [col.lower() for col in hist.columns]
            
            # Rename Date/Datetime to timestamp
            if 'date' in hist.columns:
                hist.rename(columns={'date': 'timestamp'}, inplace=True)
            elif 'datetime' in hist.columns:
                hist.rename(columns={'datetime': 'timestamp'}, inplace=True)
            
            return hist
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_market_indices(_self):
        """
        Get major market indices with caching
        
        Returns:
            dict: Index data for S&P 500, NASDAQ, DOW
        """
        indices = {
            '^GSPC': 'S&P 500',
            '^IXIC': 'NASDAQ', 
            '^DJI': 'DOW'
        }
        
        results = {}
        
        for symbol, name in indices.items():
            data = _self.get_live_price(symbol)
            if data:
                results[name] = {
                    'price': data['price'],
                    'change': data['change'],
                    'change_pct': data['change_pct']
                }
        
        return results
    
    def get_multiple_quotes(_self, symbols):
        """
        Get quotes for multiple symbols efficiently
        
        Args:
            symbols: List of ticker symbols
            
        Returns:
            dict: Symbol -> price data mapping
        """
        results = {}
        
        for symbol in symbols:
            data = _self.get_live_price(symbol)
            if data:
                results[symbol] = data
        
        return results


def generate_synthetic_fallback(symbol, days=30):
    """
    Generate synthetic data as fallback when live data fails
    This ensures the demo always works
    """
    dates = pd.date_range(end=datetime.now(), periods=days*24*4, freq='15min')
    
    # Base prices for known stocks (realistic ranges)
    base_prices = {
        'AAPL': 178.0,
        'GOOGL': 142.0,
        'MSFT': 385.0,
        'TSLA': 238.0,
        'NVDA': 502.0,
        'AMZN': 145.0,
        'META': 312.0
    }
    
    base_price = base_prices.get(symbol, np.random.uniform(50, 500))
    
    # Simulate realistic price movement
    returns = np.random.normal(0, 0.02, len(dates))
    price = base_price * (1 + returns).cumprod()
    
    # Add volatility
    price = price + np.random.normal(0, base_price*0.01, len(dates))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': price,
        'high': price * (1 + abs(np.random.normal(0, 0.005, len(dates)))),
        'low': price * (1 - abs(np.random.normal(0, 0.005, len(dates)))),
        'close': price,
        'volume': np.random.uniform(1000000, 5000000, len(dates))
    })
    
    return df


def get_market_data_hybrid(symbol, use_live=True):
    """
    Hybrid function that tries live data first, falls back to synthetic
    
    Args:
        symbol: Stock ticker symbol
        use_live: Whether to attempt live data fetch
        
    Returns:
        DataFrame: Market data (live or synthetic)
    """
    if use_live:
        try:
            live_data = LiveMarketData()
            hist = live_data.get_historical_data(symbol, period='1mo', interval='15m')
            
            if hist is not None and not hist.empty:
                return hist
        except Exception as e:
            print(f"Live data failed for {symbol}, using synthetic: {e}")
    
    # Fallback to synthetic
    return generate_synthetic_fallback(symbol)


@st.cache_data(ttl=300)
def get_portfolio_live_prices(symbols):
    """
    Get live prices for portfolio symbols with caching
    
    Args:
        symbols: List of stock symbols
        
    Returns:
        dict: Symbol -> current price mapping
    """
    live_data = LiveMarketData()
    prices = {}
    
    for symbol in symbols:
        data = live_data.get_live_price(symbol)
        if data and data['price'] > 0:
            prices[symbol] = data['price']
        else:
            # Fallback prices
            fallback_prices = {
                'AAPL': 178.32,
                'GOOGL': 142.15,
                'MSFT': 385.20,
                'TSLA': 238.75,
                'NVDA': 502.40
            }
            prices[symbol] = fallback_prices.get(symbol, 100.0)
    
    return prices

