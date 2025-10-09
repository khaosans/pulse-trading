"""
Input Validation & Data Sanitization Module
Ensures data integrity and security throughout the application
"""

from typing import Any, Optional, Union, List, Dict
import re
from datetime import datetime
import streamlit as st


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class InputValidator:
    """Validates and sanitizes user inputs"""
    
    @staticmethod
    def validate_stock_symbol(symbol: str) -> bool:
        """
        Validate stock ticker symbol
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        if not symbol:
            raise ValidationError("Stock symbol cannot be empty")
        
        # Remove whitespace
        symbol = symbol.strip().upper()
        
        # Check format: 1-5 uppercase letters, optionally with dash
        if not re.match(r'^[A-Z]{1,5}(-[A-Z]{1,2})?$', symbol):
            raise ValidationError(
                f"Invalid stock symbol: {symbol}. "
                "Must be 1-5 uppercase letters (e.g., AAPL, BRK-A)"
            )
        
        return True
    
    @staticmethod
    def validate_price(price: Union[float, str], min_value: float = 0.01) -> float:
        """
        Validate and convert price
        
        Args:
            price: Price value
            min_value: Minimum allowed price
            
        Returns:
            float: Validated price
            
        Raises:
            ValidationError: If invalid
        """
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid price: {price}. Must be a number")
        
        if price_float < min_value:
            raise ValidationError(f"Price must be at least ${min_value:.2f}")
        
        if price_float > 1_000_000:
            raise ValidationError(f"Price ${price_float:,.2f} exceeds maximum allowed")
        
        return round(price_float, 2)
    
    @staticmethod
    def validate_quantity(quantity: Union[int, str], min_value: int = 1) -> int:
        """
        Validate share quantity
        
        Args:
            quantity: Number of shares
            min_value: Minimum allowed quantity
            
        Returns:
            int: Validated quantity
            
        Raises:
            ValidationError: If invalid
        """
        try:
            quantity_int = int(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid quantity: {quantity}. Must be a whole number")
        
        if quantity_int < min_value:
            raise ValidationError(f"Quantity must be at least {min_value}")
        
        if quantity_int > 1_000_000:
            raise ValidationError(f"Quantity {quantity_int:,} exceeds maximum allowed")
        
        return quantity_int
    
    @staticmethod
    def validate_percentage(value: Union[float, str]) -> float:
        """
        Validate percentage value
        
        Args:
            value: Percentage value
            
        Returns:
            float: Validated percentage
            
        Raises:
            ValidationError: If invalid
        """
        try:
            pct = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid percentage: {value}. Must be a number")
        
        if pct < -100 or pct > 1000:
            raise ValidationError(
                f"Percentage {pct}% is out of reasonable range (-100% to 1000%)"
            )
        
        return round(pct, 2)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address
        
        Args:
            email: Email address
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        if not email:
            raise ValidationError("Email cannot be empty")
        
        email = email.strip().lower()
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError(f"Invalid email format: {email}")
        
        return True
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 1000) -> str:
        """
        Sanitize text input (remove potentially harmful characters)
        
        Args:
            text: Input text
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Truncate to max length
        text = text[:max_length]
        
        # Remove control characters except newlines/tabs
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
        
        # Remove potential HTML/script tags
        text = re.sub(r'<[^>]+>', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
        """
        Validate date range
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        if start_date >= end_date:
            raise ValidationError("Start date must be before end date")
        
        # Check if dates are reasonable (not too far in past/future)
        max_past = datetime.now().replace(year=datetime.now().year - 20)
        max_future = datetime.now().replace(year=datetime.now().year + 1)
        
        if start_date < max_past:
            raise ValidationError("Start date is too far in the past")
        
        if end_date > max_future:
            raise ValidationError("End date is too far in the future")
        
        return True


class DataValidator:
    """Validates data structures and DataFrames"""
    
    @staticmethod
    def validate_dataframe(df: Any, required_columns: List[str] = None,
                          min_rows: int = 0) -> bool:
        """
        Validate DataFrame structure
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            min_rows: Minimum number of rows required
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        import pandas as pd
        
        if not isinstance(df, pd.DataFrame):
            raise ValidationError("Data is not a valid DataFrame")
        
        if df.empty:
            raise ValidationError("DataFrame is empty")
        
        if len(df) < min_rows:
            raise ValidationError(
                f"DataFrame has {len(df)} rows, but {min_rows} required"
            )
        
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                raise ValidationError(
                    f"DataFrame missing required columns: {', '.join(missing)}"
                )
        
        return True
    
    @staticmethod
    def validate_market_data(data: Dict[str, Any]) -> bool:
        """
        Validate market data structure
        
        Args:
            data: Market data dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        required_fields = ['symbol', 'price']
        
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate price
        if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
            raise ValidationError(f"Invalid price: {data.get('price')}")
        
        # Validate symbol
        if not isinstance(data['symbol'], str) or not data['symbol']:
            raise ValidationError(f"Invalid symbol: {data.get('symbol')}")
        
        return True
    
    @staticmethod
    def validate_portfolio_data(data: Dict[str, Any]) -> bool:
        """
        Validate portfolio data structure
        
        Args:
            data: Portfolio data dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        required_fields = ['symbol', 'shares', 'avg_price', 'current_price']
        
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate numeric fields
        if data['shares'] <= 0:
            raise ValidationError("Shares must be positive")
        
        if data['avg_price'] <= 0 or data['current_price'] <= 0:
            raise ValidationError("Prices must be positive")
        
        return True


class SessionStateValidator:
    """Validates and manages session state"""
    
    @staticmethod
    def initialize_session_state(defaults: Dict[str, Any]) -> None:
        """
        Initialize session state with defaults
        
        Args:
            defaults: Dictionary of default values
        """
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def validate_session_state(required_keys: List[str]) -> bool:
        """
        Validate required session state keys exist
        
        Args:
            required_keys: List of required keys
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If invalid
        """
        missing = [key for key in required_keys if key not in st.session_state]
        
        if missing:
            raise ValidationError(
                f"Missing required session state keys: {', '.join(missing)}"
            )
        
        return True
    
    @staticmethod
    def clean_session_state(keys_to_remove: List[str] = None) -> None:
        """
        Clean up session state
        
        Args:
            keys_to_remove: Specific keys to remove, or None to remove all non-essential
        """
        if keys_to_remove:
            for key in keys_to_remove:
                if key in st.session_state:
                    del st.session_state[key]
        else:
            # Remove all except essential keys
            essential_keys = {'debug_mode', 'performance_optimized', 'perf_monitor'}
            keys_to_delete = [k for k in st.session_state.keys() if k not in essential_keys]
            for key in keys_to_delete:
                del st.session_state[key]


def safe_get(dictionary: Dict, key: str, default: Any = None,
            validator: callable = None) -> Any:
    """
    Safely get value from dictionary with validation
    
    Args:
        dictionary: Dictionary to get value from
        key: Key to retrieve
        default: Default value if key not found
        validator: Optional validation function
        
    Returns:
        Retrieved and validated value
    """
    value = dictionary.get(key, default)
    
    if validator and value is not None:
        try:
            value = validator(value)
        except (ValueError, TypeError, ValidationError):
            return default
    
    return value


def validate_and_show_error(validation_func: callable, *args, **kwargs) -> Optional[Any]:
    """
    Run validation and show error in Streamlit if it fails
    
    Args:
        validation_func: Validation function to run
        *args: Arguments to pass to validation function
        **kwargs: Keyword arguments to pass to validation function
        
    Returns:
        Validation result or None if failed
    """
    try:
        return validation_func(*args, **kwargs)
    except ValidationError as e:
        st.error(f"❌ **Validation Error**\n\n{str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ **Unexpected Error**\n\n{str(e)}")
        return None


# Example usage schemas
STOCK_TRADE_SCHEMA = {
    'symbol': InputValidator.validate_stock_symbol,
    'price': InputValidator.validate_price,
    'quantity': InputValidator.validate_quantity,
}

PORTFOLIO_SCHEMA = {
    'symbol': InputValidator.validate_stock_symbol,
    'shares': lambda x: InputValidator.validate_quantity(x, min_value=1),
    'avg_price': lambda x: InputValidator.validate_price(x, min_value=0.01),
    'current_price': lambda x: InputValidator.validate_price(x, min_value=0.01),
}


# Export commonly used validators
__all__ = [
    'ValidationError',
    'InputValidator',
    'DataValidator',
    'SessionStateValidator',
    'safe_get',
    'validate_and_show_error',
    'STOCK_TRADE_SCHEMA',
    'PORTFOLIO_SCHEMA',
]

