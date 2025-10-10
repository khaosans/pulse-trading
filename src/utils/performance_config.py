"""
Performance Configuration & Optimization Utilities
Centralizes performance settings for consistent application behavior
"""

from typing import Dict, Any
import streamlit as st
import pandas as pd

# Performance Constants
CACHE_TTL = {
    'live_data': 300,        # 5 minutes for live market data
    'historical': 900,       # 15 minutes for historical data
    'portfolio': 300,        # 5 minutes for portfolio prices
    'community': 600,        # 10 minutes for community posts
    'emotion_data': 60,      # 1 minute for emotion data (fresher)
    'market_indices': 600,   # 10 minutes for market indices
}

# UI Performance Settings
UI_CONFIG = {
    'animation_duration': 300,          # Base animation duration in ms
    'animation_duration_fast': 150,     # Fast animations
    'animation_duration_slow': 500,     # Slow animations
    'debounce_delay': 300,              # Input debounce delay
    'lazy_load_threshold': 1000,        # Lazy load after 1000px scroll
    'max_chart_points': 500,            # Max data points in charts for performance
}

# Accessibility Settings
ACCESSIBILITY_CONFIG = {
    'min_touch_target': 44,             # Minimum touch target size (px)
    'focus_outline_width': 3,           # Focus outline width (px)
    'contrast_ratio_normal': 4.5,       # WCAG AA for normal text
    'contrast_ratio_large': 3.0,        # WCAG AA for large text
}

# Mobile Breakpoints
BREAKPOINTS = {
    'mobile': 320,
    'mobile_lg': 480,
    'tablet': 768,
    'desktop': 1024,
    'desktop_lg': 1280,
    'desktop_xl': 1536,
}


def optimize_dataframe(df, max_rows: int = 1000):
    """
    Optimize DataFrame for display by limiting rows
    
    Args:
        df: Input DataFrame
        max_rows: Maximum number of rows to display
        
    Returns:
        Optimized DataFrame
    """
    if df is None or len(df) == 0:
        return df
    
    if len(df) > max_rows:
        # Sample data intelligently - keep first, last, and sample middle
        first_rows = df.head(int(max_rows * 0.3))
        last_rows = df.tail(int(max_rows * 0.3))
        middle_sample = df.iloc[len(first_rows):-len(last_rows)].sample(
            n=int(max_rows * 0.4), 
            random_state=42
        )
        return pd.concat([first_rows, middle_sample, last_rows]).sort_index()
    
    return df


def get_performance_metrics() -> Dict[str, Any]:
    """
    Get current performance metrics
    
    Returns:
        dict: Performance metrics including cache stats
    """
    return {
        'cache_enabled': True,
        'cache_ttl': CACHE_TTL,
        'ui_optimized': True,
        'accessibility_enabled': True,
    }


def apply_performance_optimizations():
    """
    Apply global performance optimizations to Streamlit app
    """
    # Set page config for optimal performance
    if 'performance_optimized' not in st.session_state:
        st.session_state.performance_optimized = True
        
        # Disable file watcher in production
        # This reduces resource usage
        
        # Enable wide mode for better use of screen space
        # Already done in main app
        
        # Set up session state defaults
        if 'data_cache' not in st.session_state:
            st.session_state.data_cache = {}
        
        if 'last_update' not in st.session_state:
            st.session_state.last_update = {}


# Consistent color scheme for data visualization
CHART_COLORS = {
    'primary': '#1D6F7A',
    'primary_light': '#2AA5B3',
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
    'neutral': '#6B7280',
}

# Consistent styling for different chart types
CHART_STYLES = {
    'line': {
        'line_width': 3,
        'line_shape': 'spline',  # Smooth lines
    },
    'candlestick': {
        'increasing_color': '#10B981',
        'decreasing_color': '#EF4444',
    },
    'bar': {
        'color_scale': ['#EF4444', '#F59E0B', '#10B981'],
    },
}

# Loading messages for better UX
LOADING_MESSAGES = [
    "Loading market data...",
    "Fetching live prices...",
    "Analyzing emotions...",
    "Updating portfolio...",
    "Syncing with wearable device...",
]


def get_loading_message(context: str = 'default') -> str:
    """
    Get contextual loading message
    
    Args:
        context: Loading context (market, portfolio, emotion, etc.)
        
    Returns:
        str: Loading message
    """
    messages = {
        'market': "📊 Loading market data...",
        'portfolio': "💼 Updating portfolio...",
        'emotion': "💓 Syncing emotional data...",
        'ai': "🤖 AI is thinking...",
        'community': "👥 Loading community feed...",
        'default': "⏳ Loading...",
    }
    return messages.get(context, messages['default'])

