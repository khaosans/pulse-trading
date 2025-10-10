"""
PulseTrade - Interactive Trading Platform Demo
A demonstration of the PulseTrade social trading platform with synthetic data

Performance Optimized | Accessible | Consistent Design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import requests
import json

# Import performance enhancements and optimizations
try:
    from src.utils import (
        initialize_enhancements, 
        enable_debug_mode,
        add_debug_panel,
        ErrorBoundary,
        format_currency,
        format_percentage
    )
    ENHANCEMENTS_AVAILABLE = True
except ImportError:
    ENHANCEMENTS_AVAILABLE = False
    print("Enhancements module not available")

# Import analytics engine
try:
    from src.analytics import (
        EmotionAnalytics,
        PortfolioAnalytics,
        MarketInsights,
        generate_daily_insights
    )
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    print("Analytics engine not available")

# Import validation and SEO
try:
    from src.utils import InputValidator, ValidationError, initialize_seo_and_meta
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False
    print("Validation module not available")

# Import new banking, freelancer, and unified analytics modules
try:
    from src.banking import AccountManager, PaymentEngine, CardManager
    from src.freelancer import InvoiceEngine, TaxManager, ExpenseTracker
    from src.analytics import CashFlowEngine, UnifiedInsights
    from src.utils.data_generator import DataGenerator
    from src.components.ui_components import (
        render_account_card, render_invoice_card, render_payment_status,
        render_tax_savings_widget, render_cash_flow_forecast,
        render_expense_category_chart, render_quick_action_button
    )
    NEW_FEATURES_AVAILABLE = True
except ImportError as e:
    NEW_FEATURES_AVAILABLE = False
    print(f"New features not available: {e}")

# Import live data module (with fallback if not available)
try:
    from src.data import LiveMarketData, get_market_data_hybrid, get_portfolio_live_prices
    LIVE_DATA_AVAILABLE = True
except ImportError:
    LIVE_DATA_AVAILABLE = False
    print("Live data module not available, using synthetic data only")

# Initialize enhancements at app start
if ENHANCEMENTS_AVAILABLE:
    enable_debug_mode()
    initialize_enhancements()

# Initialize SEO and meta tags
if VALIDATION_AVAILABLE:
    initialize_seo_and_meta()

# Page configuration
st.set_page_config(
    page_title="PulseTrade - Smart Trading Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding - Cohesive Modern Theme
st.markdown("""
<style>
    /* ============================================
       PULSETRADE DESIGN SYSTEM - UNIFIED THEME
       Modern, Clean, Highly Readable
       ============================================ */
    
    :root {
        /* Primary Palette - Teal Professional */
        --primary-color: #1D6F7A;
        --primary-light: #2AA5B3;
        --primary-dark: #155259;
        
        /* Text Colors - High Contrast */
        --text-primary: #1A202C;
        --text-secondary: #4A5568;
        --text-light: #718096;
        --text-white: #FFFFFF;
        
        /* Background Colors */
        --bg-primary: #FFFFFF;
        --bg-secondary: #F7FAFC;
        --bg-tertiary: #EDF2F7;
        
        /* Semantic Colors */
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --info: #3B82F6;
        
        /* Shadows */
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        
        /* Border Radius */
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Typography System - Highly Readable */
    .main {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
        font-size: 16px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.3;
    }
    
    h1 { font-size: 2.5rem; }
    h2 { font-size: 2rem; }
    h3 { font-size: 1.75rem; }
    h4 { font-size: 1.5rem; }
    h5 { font-size: 1.25rem; }
    h6 { font-size: 1.125rem; }
    
    p {
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Smooth Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Main Header - Animated */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        color: var(--text-white);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        animation: fadeIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        animation: shimmer 3s infinite;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.35rem;
        opacity: 0.98;
        font-weight: 500;
        position: relative;
        z-index: 1;
        color: var(--text-white);
    }
    
    /* Stat Cards - Animated & Readable */
    .stat-card {
        background: var(--bg-primary);
        padding: 2rem;
        border-radius: var(--radius-lg);
        border-left: 4px solid var(--primary-color);
        box-shadow: var(--shadow-md);
        margin: 0.75rem 0;
        transition: all var(--transition-normal);
        animation: slideIn 0.5s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-left-width: 6px;
    }
    
    .stat-value {
        font-size: 2.75rem;
        font-weight: 800;
        color: var(--primary-color);
        line-height: 1.1;
        margin: 0.75rem 0;
    }
    
    .stat-label {
        color: var(--text-light);
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .community-post {
        background: var(--card-background);
        padding: 1.25rem;
        border-radius: 10px;
        margin: 0.75rem 0;
        border-left: 4px solid var(--secondary-color);
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s ease;
    }
    
    .community-post:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .trade-signal {
        padding: 0.5rem 1.25rem;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.875rem;
        display: inline-block;
        margin: 0.25rem;
        transition: all 0.2s ease;
    }
    
    .signal-buy {
        background: #D1FAE5;
        color: #065F46;
        border: 2px solid #10B981;
    }
    
    .signal-buy:hover {
        background: #A7F3D0;
    }
    
    .signal-sell {
        background: #FEE2E2;
        color: #991B1B;
        border: 2px solid #EF4444;
    }
    
    .signal-sell:hover {
        background: #FECACA;
    }
    
    .signal-hold {
        background: #FEF3C7;
        color: #92400E;
        border: 2px solid #F59E0B;
    }
    
    .signal-hold:hover {
        background: #FDE68A;
    }
    
    .user-badge {
        background: linear-gradient(135deg, #1D6F7A 0%, #2AA5B3 100%);
        color: #FFFFFF;
        padding: 0.35rem 0.85rem;
        border-radius: 14px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Enhanced Tabs - Modern Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: var(--bg-secondary);
        padding: 0.75rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 56px;
        padding: 0 2rem;
        font-weight: 700;
        border-radius: var(--radius-md);
        font-size: 1.05rem;
        color: var(--text-secondary);
        transition: all var(--transition-fast);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--bg-tertiary);
        color: var(--primary-color);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        color: var(--text-white);
        box-shadow: var(--shadow-md);
    }
    
    .metric-container {
        background: linear-gradient(135deg, rgba(42, 165, 179, 0.08) 0%, rgba(29, 111, 122, 0.08) 100%);
        padding: 1.25rem;
        border-radius: 10px;
        border: 2px solid var(--border-color);
    }
    
    /* Improved text contrast for all elements */
    .stMarkdown {
        color: var(--text-primary);
    }
    
    .stMarkdown h3 {
        color: var(--primary-color);
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stMarkdown h4 {
        color: var(--text-primary);
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* Modern Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        color: var(--text-white);
        border: none;
        border-radius: var(--radius-md);
        padding: 0.875rem 2.5rem;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all var(--transition-normal);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.2);
        transition: left var(--transition-normal);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Improved input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
        color: var(--text-primary);
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(29, 111, 122, 0.1);
    }
    
    /* Enhanced dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Sidebar - Themed & Animated */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FAFBFC 0%, #F7FAFC 50%, #EDF2F7 100%);
        border-right: 2px solid var(--bg-tertiary);
        animation: slideIn 0.4s ease-out;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        padding: 2rem 1.5rem;
        margin: -1rem -1rem 1rem -1rem;
        border-radius: 0 0 var(--radius-xl) var(--radius-xl);
        box-shadow: var(--shadow-md);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
        font-size: 1rem;
        line-height: 1.6;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown h4 {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary-light);
        padding-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stMetric {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-normal);
    }
    
    [data-testid="stSidebar"] .stMetric:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 2px solid var(--bg-tertiary);
    }
    
    /* Accessibility improvements */
    a {
        color: var(--primary-color);
        text-decoration: underline;
    }
    
    a:hover {
        color: var(--primary-light);
    }
    
    /* Loading & Animations */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
        animation: pulse 1.5s infinite;
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-md);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Chat Container */
    .chat-container {
        background: var(--bg-primary);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        animation: fadeIn 0.5s ease-out;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: var(--radius-md);
        margin: 0.75rem 0;
        animation: slideIn 0.3s ease-out;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        color: var(--text-white);
        margin-left: 2rem;
    }
    
    .chat-message.assistant {
        background: var(--bg-secondary);
        color: var(--text-primary);
        margin-right: 2rem;
        border: 1px solid var(--bg-tertiary);
    }
    
    /* Emotion Gauge Animation */
    .emotion-gauge {
        animation: fadeIn 0.6s ease-out;
        transition: all var(--transition-normal);
    }
    
    .emotion-gauge:hover {
        transform: scale(1.05);
    }
    
    /* ============================================
       AI APPLICATION ANIMATIONS
       ============================================ */
    
    /* Animated Logo - Pulse Effect */
    @keyframes logoPulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(29, 111, 122, 0.7);
        }
        50% {
            transform: scale(1.05);
            box-shadow: 0 0 20px 10px rgba(29, 111, 122, 0);
        }
    }
    
    .logo-animated {
        animation: logoPulse 2s ease-in-out infinite;
    }
    
    /* AI Thinking Animation */
    @keyframes aiThinking {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    
    .ai-thinking {
        animation: aiThinking 1.5s ease-in-out infinite;
    }
    
    /* Skeleton Loader */
    @keyframes skeleton {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .skeleton-loader {
        background: linear-gradient(
            90deg,
            #f0f0f0 25%,
            #e0e0e0 50%,
            #f0f0f0 75%
        );
        background-size: 200% 100%;
        animation: skeleton 1.5s ease-in-out infinite;
        border-radius: 8px;
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .float-animate {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Glow Effect */
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 5px rgba(29, 111, 122, 0.5);
        }
        50% {
            box-shadow: 0 0 20px rgba(29, 111, 122, 0.8),
                        0 0 30px rgba(42, 165, 179, 0.6);
        }
    }
    
    .glow-effect {
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Card Stack Animation */
    @keyframes cardStack {
        0% {
            transform: translateY(40px) scale(0.9);
            opacity: 0;
        }
        100% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
    }
    
    .card-stack {
        animation: cardStack 0.5s ease-out backwards;
    }
    
    .card-stack:nth-child(1) { animation-delay: 0.05s; }
    .card-stack:nth-child(2) { animation-delay: 0.1s; }
    .card-stack:nth-child(3) { animation-delay: 0.15s; }
    .card-stack:nth-child(4) { animation-delay: 0.2s; }
    .card-stack:nth-child(5) { animation-delay: 0.25s; }
    .card-stack:nth-child(6) { animation-delay: 0.3s; }
    
    /* Gradient Text */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .gradient-text {
        background: linear-gradient(
            90deg,
            #1D6F7A,
            #2AA5B3,
            #10B981,
            #2AA5B3,
            #1D6F7A
        );
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
    }
    
    /* AI Processing Dots */
    @keyframes dotPulse {
        0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
        40% { opacity: 1; transform: scale(1.2); }
    }
    
    .ai-dot {
        animation: dotPulse 1.4s ease-in-out infinite;
    }
    
    .ai-dot:nth-child(1) { animation-delay: 0s; }
    .ai-dot:nth-child(2) { animation-delay: 0.2s; }
    .ai-dot:nth-child(3) { animation-delay: 0.4s; }
    
    /* Slide In Notifications */
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-slide {
        animation: slideInRight 0.4s ease-out;
    }
    
    /* 3D Card Tilt */
    .card-3d {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card-3d:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Progress Bar Animation */
    @keyframes progressLoad {
        0% { width: 0%; }
        100% { width: var(--progress-width, 100%); }
    }
    
    .progress-animate {
        animation: progressLoad 1.5s ease-out forwards;
    }
    
    /* Accessibility */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Generate synthetic data
@st.cache_data
def generate_market_data(symbol, days=30, use_live=False):
    """
    Generate market data - live or synthetic
    
    Args:
        symbol: Stock ticker symbol
        days: Number of days of data (for synthetic)
        use_live: Whether to use live data (default: False for demo reliability)
        
    Returns:
        DataFrame: Market data
    """
    # Try live data if enabled and available
    if use_live and LIVE_DATA_AVAILABLE:
        try:
            return get_market_data_hybrid(symbol, use_live=True)
        except Exception as e:
            print(f"Live data failed, using synthetic: {e}")
    
    # Synthetic data (fallback or default)
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
    
    base_price = base_prices.get(symbol, random.uniform(50, 500))
    returns = np.random.normal(0, 0.02, len(dates))
    price = base_price * (1 + returns).cumprod()
    
    # Add some volatility
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def generate_portfolio_data(use_live=False):
    """
    Generate portfolio data with optional live prices
    
    Args:
        use_live: Whether to use live prices (default: False for demo reliability)
        
    Returns:
        DataFrame: Portfolio data
    """
    positions = [
        {'symbol': 'AAPL', 'shares': 50, 'avg_price': 172.50, 'current_price': 178.32},
        {'symbol': 'GOOGL', 'shares': 25, 'avg_price': 139.80, 'current_price': 142.15},
        {'symbol': 'MSFT', 'shares': 40, 'avg_price': 378.90, 'current_price': 385.20},
        {'symbol': 'TSLA', 'shares': 15, 'avg_price': 242.30, 'current_price': 238.75},
        {'symbol': 'NVDA', 'shares': 30, 'avg_price': 485.20, 'current_price': 502.40},
    ]
    
    # Try to get live prices if enabled
    if use_live and LIVE_DATA_AVAILABLE:
        try:
            symbols = [pos['symbol'] for pos in positions]
            live_prices = get_portfolio_live_prices(symbols)
            
            # Update with live prices
            for pos in positions:
                if pos['symbol'] in live_prices:
                    pos['current_price'] = live_prices[pos['symbol']]
        except Exception as e:
            print(f"Could not fetch live prices: {e}")
    
    # Calculate metrics
    for pos in positions:
        pos['market_value'] = pos['shares'] * pos['current_price']
        pos['cost_basis'] = pos['shares'] * pos['avg_price']
        pos['gain_loss'] = pos['market_value'] - pos['cost_basis']
        pos['gain_loss_pct'] = (pos['gain_loss'] / pos['cost_basis']) * 100
    
    return pd.DataFrame(positions)

@st.cache_data
def generate_community_posts():
    """Generate synthetic community posts"""
    users = ['Sarah_Trader', 'Mike_Investor', 'Emma_Finance', 'Alex_Markets', 'Jordan_Tech']
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'META']
    
    posts = []
    for _ in range(10):
        ticker = random.choice(tickers)
        user = random.choice(users)
        sentiment = random.choice(['bullish', 'bearish', 'neutral'])
        
        if sentiment == 'bullish':
            content = f"Strong momentum on ${ticker}! Seeing great technical indicators. 🚀"
            signal = 'BUY'
        elif sentiment == 'bearish':
            content = f"Concerned about ${ticker} outlook. Might be time to take profits. 📉"
            signal = 'SELL'
        else:
            content = f"Monitoring ${ticker} closely. Waiting for clearer signals. 👀"
            signal = 'HOLD'
        
        posts.append({
            'user': user,
            'content': content,
            'ticker': ticker,
            'signal': signal,
            'likes': random.randint(5, 150),
            'comments': random.randint(2, 45),
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 48))
        })
    
    return sorted(posts, key=lambda x: x['timestamp'], reverse=True)

@st.cache_data
def generate_emotion_data():
    """Generate synthetic emotion tracking data"""
    emotions = {
        'Calm': {'value': random.uniform(60, 85), 'color': '#10B981', 'icon': '😌'},
        'Confident': {'value': random.uniform(65, 90), 'color': '#2AA5B3', 'icon': '😊'},
        'Optimistic': {'value': random.uniform(70, 95), 'color': '#3B82F6', 'icon': '😃'},
        'Anxious': {'value': random.uniform(20, 45), 'color': '#F59E0B', 'icon': '😰'},
        'Excited': {'value': random.uniform(50, 80), 'color': '#8B5CF6', 'icon': '🤩'},
        'Stressed': {'value': random.uniform(15, 35), 'color': '#EF4444', 'icon': '😓'}
    }
    return emotions

def get_free_ai_response(question, context):
    """Generate helpful trading advice using built-in logic (100% free, no external dependencies)"""
    
    question_lower = question.lower()
    
    # Emotion-related questions
    if 'anxious' in question_lower or 'anxiety' in question_lower or 'nervous' in question_lower:
        return """🛑 **Avoid Trading When Anxious**

Based on your current emotional state (Calm: 72%, Stress: Low), you're actually in a good state right now. However, when you do feel anxious:

**Our data shows**: Your win rate drops to 38% when anxious vs 72% when calm.

**Recommendation**: 
- Take a 15-minute break if anxiety rises
- Practice deep breathing exercises
- Wait until your calm level reaches 70%+
- Set strict stop-losses if you must trade

Your wearable will alert you when stress levels spike. Trust the system - it saved you $450 last time!"""
    
    elif 'stop loss' in question_lower or 'stop-loss' in question_lower:
        return """🎯 **Effective Stop-Loss Strategy**

For your current portfolio ($68,450), here's what works:

**Rule of Thumb**: Set stop-losses at 2% below entry for most trades.

**Example**: If you buy AAPL at $178.32:
- Stop-loss: $174.75 (2% down)
- Max loss: ~$87 per share

**Emotional Protection**: 
- When you're calm (like now at 72%), you can handle 2-3% stops
- When stressed, use tighter 1% stops to protect capital
- Your emotion tracker will recommend adjusting stops based on your state

**Pro Tip**: Our community's top traders (like Mike_Investor, +15.2%) always use stops. No exceptions!"""
    
    elif 'buy' in question_lower and 'time' in question_lower:
        return """⏰ **Optimal Trading Times**

Based on YOUR emotional patterns:

**Best Times for YOU**:
- Morning (9:30-11:00 AM) - You're typically 80% calm
- Mid-afternoon (2:00-3:30 PM) - High confidence levels

**Avoid Trading When**:
- Right after wake-up (emotional baseline settling)
- Late evening (fatigue affects decisions)
- During stress spikes (your tracker will alert you)

**Current Status**: You're at 72% calm, HR 68 bpm - ✅ GREEN LIGHT to trade!

**Data**: You have a 68% success rate when trading in optimal emotional windows like right now."""
    
    elif 'rsi' in question_lower:
        return """📊 **RSI Indicator Explained**

**RSI (Relative Strength Index)**: Measures momentum from 0-100.

**How to Use**:
- **Above 70**: Overbought (consider selling)
- **30-70**: Neutral zone
- **Below 30**: Oversold (consider buying)

**For AAPL** (your watchlist): Current RSI is 58.3 (Neutral)

**Combine with Emotions**: 
- If RSI says "buy" but you're anxious → WAIT
- If RSI says "sell" but you're overexcited → Good signal!
- Best trades: RSI signal + calm emotional state

**Your Edge**: Use RSI for signals, emotions for timing. 72% win rate when both align!"""
    
    elif 'risk' in question_lower or 'manage' in question_lower:
        return """🛡️ **Risk Management Essentials**

For YOUR portfolio ($68,450):

**Position Sizing**: Never risk more than 2% per trade
- Max risk per trade: $1,369
- If buying at $178, max loss $1,369 = ~16 shares with 5% stop

**Diversification**: 
- You have 5 positions (AAPL, GOOGL, MSFT, TSLA, NVDA) ✅ Good!
- No single position should exceed 30%
- Mix sectors (you have tech-heavy, consider diversifying)

**Emotional Risk Management**:
- Trade size ↓ when stress ↑
- Use 50% position size if calm < 60%
- Full size only when calm > 70% (like now!)

**Your Stats**: You've prevented 15 emotional trades this month, saving $3,240. That's risk management!"""
    
    elif 'diversif' in question_lower or 'portfolio' in question_lower:
        return """🎯 **Portfolio Diversification Tips**

**Your Current Portfolio**: 
- Tech-heavy (AAPL, GOOGL, MSFT, NVDA) 
- Total value: $68,450
- YTD: +5.2% ✅

**Recommendations**:
1. **Add Sectors**: Healthcare, Finance, Consumer goods
2. **Risk Balance**: 60% growth stocks, 30% dividend, 10% bonds
3. **Rebalance Quarterly**: When emotions are calm

**Emotion Factor**: 
- Diversify when calm (better decisions)
- Don't panic-diversify during stress
- Your tracker shows you're calm now - good time to review!

**Community Insight**: Emma_Finance (+12.8%) has 8-sector diversification. Worth following!"""
    
    else:
        # Default helpful response
        return f"""💡 **Trading Insight Based on Your State**

**Your Current Status**:
- Emotional State: Focused/Confident (72% calm)
- Portfolio: $68,450 (+5.2% today, +$892)
- Heart Rate: 68 bpm (optimal range)
- Recent Alert: Prevented panic sell, saved $450

**General Guidance**:
✅ **Green Light to Trade** - Your emotional state is optimal
- Win rate in this state: 68%
- Stress level: Low
- Confidence: High

**Quick Tips**:
1. Set stop-losses at 2% for protection
2. Trade only watchlist stocks (AAPL, GOOGL, MSFT, TSLA, NVDA)
3. Check community sentiment before large trades
4. Trust your emotion alerts - they've saved you $3,240 this month!

**Question**: "{question[:100]}"

*For specific questions, try asking about: stop losses, risk management, RSI indicators, or timing your trades.*"""

def query_ollama(prompt, model="llama2"):
    """Query local Ollama model for AI responses, with free fallback"""
    
    # Try Ollama first (if available)
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False
            },
            timeout=10  # Reduced timeout
        )
        
        if response.status_code == 200:
            return response.json().get('response', 'Error: No response generated')
    except:
        pass  # Fall through to free AI
    
    # Extract question from context
    question = ""
    if "User question:" in prompt:
        question = prompt.split("User question:")[1].strip()
    else:
        question = prompt
    
    # Use free built-in AI (no external dependencies)
    return get_free_ai_response(question, prompt)

@st.cache_data
def generate_emotion_history():
    """Generate historical emotion vs performance data"""
    hours = 24
    times = pd.date_range(end=datetime.now(), periods=hours, freq='H')
    
    # Generate correlated data - high stress correlates with poor decisions
    stress_levels = np.random.uniform(20, 80, hours)
    calm_levels = 100 - stress_levels + np.random.normal(0, 10, hours)
    
    # Performance inversely correlated with stress
    performance = -0.5 * stress_levels + np.random.normal(50, 15, hours)
    
    df = pd.DataFrame({
        'Time': times,
        'Stress': stress_levels,
        'Calm': calm_levels,
        'Performance': performance,
        'Heart_Rate': np.random.uniform(65, 95, hours),
    })
    
    return df

def create_price_chart(df, symbol):
    """Create interactive price chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=symbol
    ))
    
    # Add moving averages
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'], 
        y=df['MA20'], 
        name='MA20',
        line=dict(color='#2AA5B3', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'], 
        y=df['MA50'], 
        name='MA50',
        line=dict(color='#1D6F7A', width=2)
    ))
    
    fig.update_layout(
        title=dict(
            text=f'{symbol} Price Chart',
            font=dict(size=20, color='#0F2B33', family='Arial, sans-serif')
        ),
        yaxis_title='Price ($)',
        xaxis_title='Date',
        height=500,
        template='plotly_white',
        hovermode='x unified',
        font=dict(size=12, color='#4A5F66'),
        plot_bgcolor='#F8F9FA',
        paper_bgcolor='#FFFFFF'
    )
    
    return fig

def create_portfolio_pie(portfolio_df):
    """Create portfolio allocation pie chart"""
    fig = px.pie(
        portfolio_df, 
        values='market_value', 
        names='symbol',
        title='Portfolio Allocation',
        color_discrete_sequence=px.colors.sequential.Teal
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig

# Main app
def main():
    # Header with animated gradient text
    if NEW_FEATURES_AVAILABLE:
        tagline = "Complete Financial OS for Freelancers • Banking + Business + Wealth + Emotion Intelligence"
    else:
        tagline = "Smart Trading Through Data + Community"
    
    st.markdown(f"""
    <div class="main-header">
        <h1 class="gradient-text">📊 PulseTrade</h1>
        <p style="font-size: 1.2rem; margin: 0;">{tagline}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Logo and Welcome Section
        col_logo, col_text = st.columns([1, 2])
        with col_logo:
            # Try to use local logo, fallback to animated placeholder
            try:
                st.image("assets/images/logo.svg", width=80)
            except:
                st.markdown("""
                <div class="logo-animated float-animate" style="width: 80px; height: 80px; background: linear-gradient(135deg, #1D6F7A 0%, #2AA5B3 100%); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            font-size: 2rem; color: white; font-weight: 800;">PT</div>
                """, unsafe_allow_html=True)
        
        with col_text:
            st.markdown("""
            <div style="padding-top: 0.5rem;">
                <div style="font-size: 1.4rem; font-weight: 800; color: var(--text-white); margin-bottom: 0.25rem;">
                    PulseTrade
                </div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.9); font-weight: 500;">
                    Emotion-Aware Trading
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 1rem; text-align: center;">
            <div style="color: var(--text-white); font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
                Welcome, Sarah! 👋
            </div>
            <span class="user-badge">PREMIUM MEMBER</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Emotion Wearable Status
        st.markdown("#### 💓 Emotion Tracker")
        
        current_emotion = random.choice(['Calm', 'Confident', 'Optimistic', 'Focused'])
        emotion_icons = {
            'Calm': '😌',
            'Confident': '😊', 
            'Optimistic': '😃',
            'Focused': '🎯'
        }
        
        st.markdown(f"""
        <div class="glow-effect" style="background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); 
                    padding: 1.5rem; border-radius: var(--radius-lg); text-align: center; margin-bottom: 1.5rem;
                    border: 3px solid #10B981; box-shadow: var(--shadow-md);
                    animation: fadeIn 0.6s ease-out;">
            <div class="float-animate" style="font-size: 2.5rem; margin-bottom: 0.75rem;">{emotion_icons[current_emotion]}</div>
            <div style="font-weight: 800; color: #065F46; font-size: 1.3rem; margin-bottom: 0.5rem;">{current_emotion}</div>
            <div style="font-size: 0.9rem; color: #047857; font-weight: 600;">
                <span class="ai-dot" style="display: inline-block; width: 8px; height: 8px; background: #10B981; border-radius: 50%; margin-right: 4px;"></span>
                Device Connected
            </div>
            <div style="font-size: 0.8rem; color: #059669; margin-top: 0.25rem;">
                ⚡ Syncing every 2 seconds
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Vital Signs
        st.markdown("#### 💓 Live Vitals")
        heart_rate = random.randint(68, 85)
        hrv = random.randint(45, 75)
        
        st.markdown(f"""
        <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                    box-shadow: var(--shadow-sm); margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="color: var(--text-secondary); font-weight: 600; font-size: 0.95rem;">❤️ Heart Rate</span>
                <span style="color: var(--primary-color); font-weight: 800; font-size: 1.3rem;">{heart_rate}</span>
            </div>
            <div style="color: var(--text-light); font-size: 0.85rem; text-align: right;">bpm</div>
        </div>
        
        <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                    box-shadow: var(--shadow-sm);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="color: var(--text-secondary); font-weight: 600; font-size: 0.95rem;">📊 HRV</span>
                <span style="color: var(--primary-color); font-weight: 800; font-size: 1.3rem;">{hrv}</span>
            </div>
            <div style="color: var(--text-light); font-size: 0.85rem; text-align: right;">ms</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Live Data Toggle
        st.markdown("#### 📡 Data Source")
        
        use_live_data = st.toggle(
            "🔴 Live Market Data",
            value=False,
            help="Enable real-time market data from Yahoo Finance (updates every 5min). Disable for faster, reliable demo mode.",
            key="live_data_toggle"
        )
        
        if use_live_data:
            if LIVE_DATA_AVAILABLE:
                st.success("✅ Live data active (cached 5min)")
            else:
                st.warning("⚠️ yfinance not installed. Using demo data.")
                use_live_data = False
        else:
            st.info("📊 Demo mode (synthetic data)")
        
        # Store in session state for use across tabs
        st.session_state['use_live_data'] = use_live_data if LIVE_DATA_AVAILABLE else False
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("#### 📊 Your Quick Stats")
        
        if NEW_FEATURES_AVAILABLE:
            # Calculate total net worth
            bank_balance = st.session_state.get('bank_account', {}).get('balance', 25000)
            tax_balance = st.session_state.get('tax_pot', {}).get('balance', 8500)
            portfolio_value = 68450
            invoices_df = st.session_state.get('invoices_df', pd.DataFrame())
            outstanding = invoices_df[invoices_df['status'] != 'paid']['total'].sum() if not invoices_df.empty else 0
            total_net_worth = bank_balance + tax_balance + portfolio_value + outstanding
            
            st.markdown(f"""
            <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                        box-shadow: var(--shadow-sm); margin-bottom: 0.75rem;">
                <div style="color: var(--text-light); font-size: 0.85rem; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                    Total Net Worth
                </div>
                <div style="color: var(--primary-color); font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem;">
                    ${total_net_worth:,.0f}
                </div>
                <div style="color: #10B981; font-weight: 700; font-size: 1rem;">
                    Business + Trading
                </div>
            </div>
            
            <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                        box-shadow: var(--shadow-sm); margin-bottom: 0.75rem;">
                <div style="color: var(--text-light); font-size: 0.85rem; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                    Business Cash
                </div>
                <div style="color: var(--primary-color); font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem;">
                    ${bank_balance:,.0f}
                </div>
                <div style="color: #718096; font-weight: 600; font-size: 0.9rem;">
                    Tax Pot: ${tax_balance:,.0f}
                </div>
            </div>
            
            <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                        box-shadow: var(--shadow-sm);">
                <div style="color: var(--text-light); font-size: 0.85rem; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                    Today's Activity
                </div>
                <div style="color: var(--primary-color); font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem;">
                    +$3,392
                </div>
                <div style="color: #10B981; font-weight: 700; font-size: 1rem;">
                    Invoice + Trading
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Original stats for trading-only version
            st.markdown("""
            <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                        box-shadow: var(--shadow-sm); margin-bottom: 0.75rem;">
                <div style="color: var(--text-light); font-size: 0.85rem; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                    Portfolio Value
                </div>
                <div style="color: var(--primary-color); font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem;">
                    $68,450
                </div>
                <div style="color: #10B981; font-weight: 700; font-size: 1rem;">
                    +5.2% ↑
                </div>
            </div>
            
            <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md);
                        box-shadow: var(--shadow-sm);">
                <div style="color: var(--text-light); font-size: 0.85rem; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                    Today's P/L
                </div>
                <div style="color: var(--primary-color); font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem;">
                    +$892
                </div>
                <div style="color: #10B981; font-weight: 700; font-size: 1rem;">
                    +1.3% ↑
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Watchlist
        st.markdown("#### 📌 Watchlist")
        watchlist = [
            ('AAPL', 2.45, 178.32),
            ('GOOGL', -1.23, 142.15),
            ('MSFT', 3.67, 385.20),
            ('TSLA', -4.32, 238.75),
            ('NVDA', 5.21, 502.40)
        ]
        
        for ticker, change, price in watchlist:
            color = "#10B981" if change > 0 else "#EF4444"
            icon = "🟢" if change > 0 else "🔴"
            
            st.markdown(f"""
            <div style="background: var(--bg-primary); padding: 0.75rem; border-radius: var(--radius-md); 
                        margin: 0.5rem 0; border-left: 3px solid {color}; box-shadow: var(--shadow-sm);
                        transition: all var(--transition-normal);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 1.05rem;">
                        {icon} {ticker}
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {color}; font-weight: 700; font-size: 1rem;">
                            {change:+.2f}%
                        </div>
                        <div style="color: var(--text-light); font-size: 0.85rem;">
                            ${price:.2f}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🔔 Alerts")
        
        st.markdown("""
        <div style="background: #D1FAE5; padding: 1rem; border-radius: var(--radius-md); 
                    margin: 0.5rem 0; border-left: 3px solid #10B981;">
            <div style="color: #065F46; font-weight: 700; font-size: 0.95rem;">
                ✅ AAPL crossed $178 resistance
            </div>
            <div style="color: #047857; font-size: 0.85rem; margin-top: 0.25rem;">
                2 mins ago • Bullish signal
            </div>
        </div>
        
        <div style="background: #FEF3C7; padding: 1rem; border-radius: var(--radius-md); 
                    margin: 0.5rem 0; border-left: 3px solid #F59E0B;">
            <div style="color: #92400E; font-weight: 700; font-size: 0.95rem;">
                ⚠️ TSLA volume spike detected
            </div>
            <div style="color: #78350F; font-size: 0.85rem; margin-top: 0.25rem;">
                5 mins ago • Monitor closely
            </div>
        </div>
        
        <div style="background: #DBEAFE; padding: 1rem; border-radius: var(--radius-md); 
                    margin: 0.5rem 0; border-left: 3px solid #3B82F6;">
            <div style="color: #1E40AF; font-weight: 700; font-size: 0.95rem;">
                💓 Emotion Alert: Stay Calm
            </div>
            <div style="color: #1E3A8A; font-size: 0.85rem; margin-top: 0.25rem;">
                Your stress is rising • Take a breath
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add debug panel if enhancements are available
    if ENHANCEMENTS_AVAILABLE:
        add_debug_panel()
    
    # Generate synthetic data for new features (if available)
    if NEW_FEATURES_AVAILABLE:
        if 'bank_account' not in st.session_state:
            st.session_state['bank_account'] = DataGenerator.generate_bank_account()
            st.session_state['tax_pot'] = DataGenerator.generate_tax_pot_account()
            st.session_state['invoices_df'] = DataGenerator.generate_invoices(10)
            st.session_state['expenses_df'] = DataGenerator.generate_expenses(30)
            st.session_state['transactions_df'] = DataGenerator.generate_transactions(30)
            st.session_state['clients_df'] = DataGenerator.generate_clients(10)
    
    # Main content tabs - Enhanced with new features!
    if NEW_FEATURES_AVAILABLE:
        tabs = st.tabs([
            "🏦 Dashboard", 
            "💓 Emotion Tracker",
            "💸 Banking",
            "🧾 Invoicing",
            "🧮 Tax & Expenses",
            "📈 Cash Flow",
            "📊 Trading & Portfolio",
            "🤖 AI Assistant",
            "👥 Community", 
            "🎓 Learn"
        ])
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = tabs
    else:
        # Fallback to original tabs if new features not available
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Dashboard", 
            "💓 Emotion Tracker",
            "🤖 AI Assistant",
            "💼 Portfolio & Analysis", 
            "👥 Community", 
            "🎓 Learn"
        ])
    
    with tab1:
        if NEW_FEATURES_AVAILABLE:
            # UNIFIED FINANCIAL DASHBOARD
            st.markdown("### 💼 Your Complete Financial Overview")
            
            # Calculate total net worth
            bank_balance = st.session_state.get('bank_account', {}).get('balance', 25000)
            tax_balance = st.session_state.get('tax_pot', {}).get('balance', 8500)
            portfolio_value = 68450  # From trading
            invoices_outstanding = st.session_state.get('invoices_df', pd.DataFrame()).query('status != "paid"')['total'].sum() if not st.session_state.get('invoices_df', pd.DataFrame()).empty else 12000
            
            total_net_worth = bank_balance + tax_balance + portfolio_value + invoices_outstanding
            
            # Top financial metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card card-stack card-3d">
                    <div class="stat-label">Total Net Worth</div>
                    <div class="stat-value">${total_net_worth:,.0f}</div>
                    <div style="color: #059669; font-weight: 700; font-size: 1.1rem;">+$4,892 ↑</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card card-stack card-3d">
                    <div class="stat-label">Business Cash</div>
                    <div class="stat-value">${bank_balance:,.0f}</div>
                    <div style="color: #059669; font-weight: 700; font-size: 1.1rem;">Available</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card card-stack card-3d">
                    <div class="stat-label">Investment Portfolio</div>
                    <div class="stat-value">${portfolio_value:,.0f}</div>
                    <div style="color: #059669; font-weight: 700; font-size: 1.1rem;">+5.2% ↑</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card card-stack card-3d">
                    <div class="stat-label">Receivables</div>
                    <div class="stat-value">${invoices_outstanding:,.0f}</div>
                    <div style="color: #F59E0B; font-weight: 700; font-size: 1.1rem;">Due Soon</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Today's Activity & Quick Actions
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📊 Today's Activity")
                
                # Business activity
                st.markdown("""
                <div class="card" style="padding: 1.5rem; margin-bottom: 1rem;">
                    <h4 style="color: #1D6F7A; margin-top: 0;">💼 Business</h4>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>✅ Invoice #1023 paid</span>
                        <span style="color: #10B981; font-weight: 700;">+$2,500</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>📤 Sent 2 invoices</span>
                        <span style="color: #718096;">$5,400</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>💳 Business expenses</span>
                        <span style="color: #EF4444;">-$287</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Trading activity
                st.markdown("""
                <div class="card" style="padding: 1.5rem;">
                    <h4 style="color: #1D6F7A; margin-top: 0;">📈 Trading & Investments</h4>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Portfolio performance</span>
                        <span style="color: #10B981; font-weight: 700;">+$892</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>AAPL position</span>
                        <span style="color: #10B981;">+2.45%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Emotion prevented 1 trade</span>
                        <span style="color: #10B981;">Saved $450</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### ⚡ Quick Actions")
                
                if st.button("💸 Send Payment", use_container_width=True):
                    st.info("Navigate to Banking tab to send payments")
                
                if st.button("🧾 Create Invoice", use_container_width=True):
                    st.info("Navigate to Invoicing tab to create invoices")
                
                if st.button("📊 View Cash Flow", use_container_width=True):
                    st.info("Navigate to Cash Flow tab for forecasting")
                
                if st.button("📈 Make Trade", use_container_width=True):
                    st.info("Navigate to Trading tab to execute trades")
                
                st.markdown("---")
                
                # Emotion status
                current_emotion = random.choice(['Calm', 'Confident', 'Optimistic'])
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); 
                            padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">😌</div>
                    <div style="font-weight: 700; color: #065F46; font-size: 1.1rem;">{current_emotion}</div>
                    <div style="color: #047857; font-size: 0.875rem; margin-top: 0.5rem;">✅ Optimal for decisions</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Upcoming & Alerts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📅 Upcoming This Week")
                st.markdown("""
                - 💰 Q4 Estimated Tax Due (Jan 15) - $7,200
                - 🧾 Follow up: Invoice #1019 (overdue 3 days)
                - 💳 Adobe subscription renewal - $79.99
                - 📊 Review cash flow forecast
                """)
            
            with col2:
                st.markdown("### 🎯 Smart Recommendations")
                st.success("✅ Transfer $2,500 from today's payment to tax pot")
                st.info("💡 Your cash flow is strong - consider investing surplus")
                st.warning("⚠️ 2 invoices overdue - send friendly reminders")
        
        else:
            # Original dashboard for fallback
            st.markdown("### Market Overview")
            
            # Top metrics with stacked animation
            col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stat-card card-stack card-3d">
                <div class="stat-label">S&P 500</div>
                <div class="stat-value">4,582.23</div>
                <div style="color: #059669; font-weight: 700; font-size: 1.1rem;">+0.85% ↑</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card card-stack card-3d">
                <div class="stat-label">NASDAQ</div>
                <div class="stat-value">14,265.86</div>
                <div style="color: #059669; font-weight: 700; font-size: 1.1rem;">+1.24% ↑</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card card-stack card-3d">
                <div class="stat-label">DOW</div>
                <div class="stat-value">35,908.42</div>
                <div style="color: #DC2626; font-weight: 700; font-size: 1.1rem;">-0.32% ↓</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-card card-stack card-3d">
                <div class="stat-label">VIX</div>
                <div class="stat-value">13.45</div>
                <div style="color: #DC2626; font-weight: 700; font-size: 1.1rem;">+2.1% ↑</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Trending stocks
        st.markdown("### 🔥 Trending Stocks")
        
        trending_data = pd.DataFrame({
            'Symbol': ['AAPL', 'NVDA', 'MSFT', 'GOOGL', 'TSLA'],
            'Price': [178.32, 502.40, 385.20, 142.15, 238.75],
            'Change': [2.45, 8.92, -1.23, 3.67, -4.32],
            'Volume': ['52.3M', '38.7M', '24.1M', '18.5M', '105.2M'],
            'Community Sentiment': ['🟢 Bullish', '🟢 Bullish', '🟡 Neutral', '🟢 Bullish', '🔴 Bearish']
        })
        
        st.dataframe(
            trending_data,
            width='stretch',
            hide_index=True
        )
        
        # Live price chart
        st.markdown("### 📊 Live Price Action")
        selected_symbol = st.selectbox("Select Stock", ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA'])
        
        # Get data source preference
        use_live = st.session_state.get('use_live_data', False)
        
        # Show data source indicator
        if use_live and LIVE_DATA_AVAILABLE:
            st.caption("📡 Showing real-time Yahoo Finance data (5min cache)")
        else:
            st.caption("📊 Showing demo data for reliable presentation")
        
        market_data = generate_market_data(selected_symbol, use_live=use_live)
        price_chart = create_price_chart(market_data, selected_symbol)
        st.plotly_chart(price_chart, use_container_width=True, key='price_chart')
        
        # AI Insights
        st.markdown("### 🤖 AI-Powered Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **{selected_symbol} Technical Analysis**
            - RSI: 58.3 (Neutral)
            - MACD: Bullish crossover
            - Support: $172.50
            - Resistance: $182.00
            - Recommendation: BUY on pullback
            """)
        
        with col2:
            st.success(f"""
            **Community Consensus**
            - 73% Bullish
            - Average Target: $195.00
            - Top Traders: 8/10 Long
            - Sentiment Score: 7.8/10
            """)
    
    with tab2:
        st.markdown("### 💓 Real-Time Emotion Tracking")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(42, 165, 179, 0.1) 0%, rgba(29, 111, 122, 0.1) 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #1D6F7A;">
            <h4 style="color: #1D6F7A; margin-top: 0;">🎯 Your PulseTrade Wearable</h4>
            <p style="margin-bottom: 0; color: #4A5F66;">
                Track your emotional state in real-time while trading. Our AI-powered wearable monitors heart rate,
                HRV, and skin conductance to detect stress, anxiety, and overconfidence—helping you make rational decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Device Status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stat-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">⌚</div>
                <div class="stat-label">Device Status</div>
                <div style="color: #10B981; font-weight: 700; font-size: 1.1rem;">● Connected</div>
                <div style="color: #6B7280; font-size: 0.85rem; margin-top: 0.5rem;">Battery: 87%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">❤️</div>
                <div class="stat-label">Heart Rate</div>
                <div class="stat-value" style="font-size: 1.75rem;">72 bpm</div>
                <div style="color: #10B981; font-size: 0.85rem; margin-top: 0.5rem;">↓ -3 from avg</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧘</div>
                <div class="stat-label">Stress Level</div>
                <div class="stat-value" style="font-size: 1.75rem; color: #10B981;">Low</div>
                <div style="color: #6B7280; font-size: 0.85rem; margin-top: 0.5rem;">Optimal for trading</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Current Emotional State
        st.markdown("### Current Emotional State")
        
        emotions = generate_emotion_data()
        
        # Create emotion gauges
        col1, col2, col3 = st.columns(3)
        
        emotion_items = list(emotions.items())
        for idx, (emotion, data) in enumerate(emotion_items[:3]):
            with [col1, col2, col3][idx]:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            border: 2px solid #E1E8EB; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{data['icon']}</div>
                    <div style="font-weight: 700; color: #0F2B33; font-size: 1.1rem; margin-bottom: 0.5rem;">
                        {emotion}
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: {data['color']};">
                        {int(data['value'])}%
                    </div>
                    <div style="width: 100%; background: #E1E8EB; height: 8px; border-radius: 4px; margin-top: 1rem;">
                        <div style="width: {data['value']}%; background: {data['color']}; 
                                    height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        for idx, (emotion, data) in enumerate(emotion_items[3:]):
            with [col1, col2, col3][idx]:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            border: 2px solid #E1E8EB; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{data['icon']}</div>
                    <div style="font-weight: 700; color: #0F2B33; font-size: 1.1rem; margin-bottom: 0.5rem;">
                        {emotion}
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: {data['color']};">
                        {int(data['value'])}%
                    </div>
                    <div style="width: 100%; background: #E1E8EB; height: 8px; border-radius: 4px; margin-top: 1rem;">
                        <div style="width: {data['value']}%; background: {data['color']}; 
                                    height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Emotion vs Performance Chart
        st.markdown("### 📊 Emotion Impact on Trading Performance (Last 24 Hours)")
        
        emotion_history = generate_emotion_history()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=emotion_history['Time'],
            y=emotion_history['Stress'],
            name='Stress Level',
            line=dict(color='#EF4444', width=2),
            fill='tonexty'
        ))
        
        fig.add_trace(go.Scatter(
            x=emotion_history['Time'],
            y=emotion_history['Calm'],
            name='Calm Level',
            line=dict(color='#10B981', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=emotion_history['Time'],
            y=emotion_history['Performance'],
            name='Trading Performance',
            line=dict(color='#2AA5B3', width=3, dash='dash'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Emotion Levels vs Trading Performance',
            xaxis_title='Time',
            yaxis_title='Emotion Level (%)',
            yaxis2=dict(
                title='Performance Score',
                overlaying='y',
                side='right'
            ),
            height=400,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, key='emotion_chart')
        
        # Insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #FEF3C7; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #F59E0B;">
                <h4 style="color: #92400E; margin-top: 0;">⚠️ Emotion Alert</h4>
                <p style="color: #78350F; margin-bottom: 0;">
                    Your stress levels spiked at 2:30 PM when TSLA dropped 3%. 
                    The system recommended a 15-minute break—you saved $450 by not panic selling!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #D1FAE5; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #10B981;">
                <h4 style="color: #065F46; margin-top: 0;">✅ Best Trading Window</h4>
                <p style="color: #047857; margin-bottom: 0;">
                    Your optimal trading performance occurs when calm levels are above 70%. 
                    Current state is perfect for making important decisions!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Trading Recommendations
        st.markdown("### 🎯 AI-Powered Recommendations")
        
        st.info("""
        **Based on your current emotional state:**
        
        ✅ **Green Light to Trade** - Your stress levels are low and confidence is high  
        📊 Your average win rate is 68% when trading in this emotional state  
        💡 **Tip**: Set a stop-loss at -2% to protect against emotional override  
        ⏰ **Optimal Window**: Next 2-3 hours based on your historical patterns
        """)
        
        # Historical Stats
        st.markdown("### 📈 Your Emotional Trading Stats (Last 30 Days)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Calm Trades", "87%", "+12%", help="Trades made while emotionally calm")
        with col2:
            st.metric("Avg Win Rate (Calm)", "72%", "+8%", help="Success rate when calm")
        with col3:
            st.metric("Stress Prevented", "15", help="Trades stopped by emotion alerts")
        with col4:
            st.metric("Money Saved", "$3,240", help="Est. savings from emotion alerts")
    
    # NEW BANKING TAB (tab3)
    if NEW_FEATURES_AVAILABLE:
        with tab3:
            st.markdown("### 💸 Banking & Payments")
            
            # Account Overview
            col1, col2 = st.columns(2)
            
            with col1:
                account = st.session_state.get('bank_account', {})
                render_account_card(account)
            
            with col2:
                tax_pot = st.session_state.get('tax_pot', {})
                render_account_card(tax_pot)
            
            st.markdown("---")
            
            # Payment Actions
            st.markdown("### 💳 Send Money")
            
            tab_ach, tab_wire, tab_p2p = st.tabs(["ACH Transfer", "Wire Transfer", "P2P Payment"])
            
            with tab_ach:
                with st.form("ach_form"):
                    recipient_name = st.text_input("Recipient Name")
                    routing = st.text_input("Routing Number", placeholder="9 digits")
                    account_num = st.text_input("Account Number")
                    amount = st.number_input("Amount ($)", min_value=0.01, step=100.0)
                    description = st.text_input("Description (optional)")
                    
                    if st.form_submit_button("Send ACH Transfer", use_container_width=True):
                        if amount > 0 and routing and account_num:
                            payment = PaymentEngine.initiate_ach_transfer(
                                from_account=account.get('account_id', 'acc_demo'),
                                to_account=recipient_name,
                                routing_number=routing,
                                account_number=account_num,
                                amount=amount,
                                description=description
                            )
                            st.success(f"✅ ACH transfer initiated! Expected completion: {payment['estimated_days']} business days")
                            render_payment_status(payment)
                        else:
                            st.error("Please fill in all required fields")
            
            with tab_wire:
                with st.form("wire_form"):
                    st.info("💡 Wire transfers complete same-day if initiated before 2 PM ET ($25-35 fee)")
                    recipient_name = st.text_input("Recipient Name")
                    routing = st.text_input("Routing Number")
                    account_num = st.text_input("Account Number")
                    amount = st.number_input("Amount ($)", min_value=0.01, step=500.0)
                    description = st.text_input("Wire Description")
                    
                    if st.form_submit_button("Send Wire Transfer", use_container_width=True):
                        if amount > 0:
                            payment = PaymentEngine.initiate_wire_transfer(
                                from_account=account.get('account_id', 'acc_demo'),
                                to_account=recipient_name,
                                routing_number=routing,
                                account_number=account_num,
                                amount=amount,
                                description=description
                            )
                            st.success(f"✅ Wire transfer initiated! Fee: ${payment['fee']:.2f}")
                            render_payment_status(payment)
            
            with tab_p2p:
                with st.form("p2p_form"):
                    st.info("💡 P2P payments are instant and free!")
                    email = st.text_input("Recipient Email")
                    amount = st.number_input("Amount ($)", min_value=0.01, step=50.0)
                    description = st.text_input("What's this for?")
                    
                    if st.form_submit_button("Send P2P Payment", use_container_width=True):
                        if amount > 0 and email:
                            payment = PaymentEngine.initiate_p2p_transfer(
                                from_account=account.get('account_id', 'acc_demo'),
                                to_email=email,
                                amount=amount,
                                description=description
                            )
                            st.success(f"✅ ${amount:,.2f} sent instantly to {email}!")
                            render_payment_status(payment)
            
            st.markdown("---")
            
            # Recent Transactions
            st.markdown("### 📜 Recent Transactions")
            transactions_df = st.session_state.get('transactions_df', pd.DataFrame())
            if not transactions_df.empty:
                st.dataframe(
                    transactions_df.head(10)[['date', 'description', 'amount', 'category', 'status']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No transactions yet")
    
    # NEW INVOICING TAB (tab4)
    if NEW_FEATURES_AVAILABLE:
        with tab4:
            st.markdown("### 🧾 Invoicing & Collections")
            
            # Create Invoice Section
            with st.expander("✍️ Create New Invoice", expanded=False):
                with st.form("invoice_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        client_name = st.text_input("Client Name", placeholder="Acme Corporation")
                        client_email = st.text_input("Client Email", placeholder="billing@acme.com")
                    
                    with col2:
                        payment_terms = st.selectbox("Payment Terms", ["net_30", "net_15", "net_45", "due_on_receipt"])
                        issue_date = st.date_input("Issue Date", datetime.now())
                    
                    st.markdown("#### Line Items")
                    description = st.text_input("Service Description", placeholder="Website Design")
                    quantity = st.number_input("Hours/Quantity", min_value=1, value=10)
                    unit_price = st.number_input("Rate/Price ($)", min_value=0.01, value=150.0)
                    
                    notes = st.text_area("Notes (optional)", placeholder="Thank you for your business!")
                    
                    if st.form_submit_button("Create & Send Invoice", use_container_width=True):
                        line_items = [{
                            'description': description,
                            'quantity': quantity,
                            'unit_price': unit_price
                        }]
                        
                        invoice = InvoiceEngine.create_invoice(
                            client_id=f"client_{hash(client_name) % 10000}",
                            client_name=client_name,
                            client_email=client_email,
                            line_items=line_items,
                            payment_terms=payment_terms,
                            notes=notes
                        )
                        
                        st.success(f"✅ Invoice {invoice['invoice_number']} created and sent!")
                        st.info(f"📎 Payment link: {invoice['payment_link']}")
                        
                        # Add to session state
                        new_invoice = pd.DataFrame([invoice])
                        st.session_state['invoices_df'] = pd.concat([st.session_state.get('invoices_df', pd.DataFrame()), new_invoice], ignore_index=True)
            
            st.markdown("---")
            
            # Invoice List
            st.markdown("### 📋 Your Invoices")
            invoices_df = st.session_state.get('invoices_df', pd.DataFrame())
            
            if not invoices_df.empty:
                # Filter options
                status_filter = st.selectbox("Filter by Status", ["All", "paid", "sent", "overdue", "draft"])
                
                if status_filter != "All":
                    filtered = invoices_df[invoices_df['status'] == status_filter]
                else:
                    filtered = invoices_df
                
                # Display invoices
                for _, invoice in filtered.head(5).iterrows():
                    render_invoice_card(invoice.to_dict())
                
                # Invoice Analytics
                st.markdown("---")
                st.markdown("### 📊 Invoice Analytics")
                
                col1, col2, col3 = st.columns(3)
                
                total_invoiced = invoices_df['total'].sum()
                total_paid = invoices_df[invoices_df['status'] == 'paid']['total'].sum()
                outstanding = total_invoiced - total_paid
                
                with col1:
                    st.metric("Total Invoiced", f"${total_invoiced:,.2f}")
                with col2:
                    st.metric("Paid", f"${total_paid:,.2f}", f"{(total_paid/total_invoiced*100):.0f}%")
                with col3:
                    st.metric("Outstanding", f"${outstanding:,.2f}")
            else:
                st.info("No invoices yet. Create your first invoice above!")
    
    # NEW TAX & EXPENSES TAB (tab5)
    if NEW_FEATURES_AVAILABLE:
        with tab5:
            st.markdown("### 🧮 Tax Management & Expenses")
            
            # Tax Summary
            st.markdown("#### 💰 Tax Savings Status")
            
            expenses_df = st.session_state.get('expenses_df', pd.DataFrame())
            total_expenses = expenses_df['amount'].sum() if not expenses_df.empty else 5000
            tax_estimate = TaxManager.estimate_taxes(gross_income=100000, deductible_expenses=total_expenses)
            
            col1, col2 = st.columns(2)
            
            with col1:
                tax_pot_balance = st.session_state.get('tax_pot', {}).get('balance', 8500)
                render_tax_savings_widget({
                    'saved': tax_pot_balance,
                    'recommended': tax_estimate['quarterly_payment'] * 3  # 3 quarters so far
                })
            
            with col2:
                st.markdown("""
                <div class="card" style="padding: 1.5rem;">
                    <h4 style="color: #1D6F7A; margin-top: 0;">📅 Quarterly Estimates</h4>
                    <div style="margin: 1rem 0;">
                        <div style="font-size: 0.875rem; color: #718096;">Next Payment Due</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #1D6F7A; margin: 0.5rem 0;">
                            Jan 15, 2025
                        </div>
                        <div style="font-size: 1.25rem; font-weight: 600;">
                            $7,200
                        </div>
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E5E7EB;">
                        <div style="font-size: 0.875rem; color: #718096;">Estimated Annual Tax</div>
                        <div style="font-weight: 700; color: #1D6F7A;">
                            ${tax_estimate['total_estimated_tax']:,.0f}
                        </div>
                        <div style="font-size: 0.75rem; color: #718096; margin-top: 0.25rem;">
                            Effective rate: {tax_estimate['effective_tax_rate']:.1f}%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Expense Tracking
            st.markdown("#### 📊 Business Expenses")
            
            if not expenses_df.empty:
                # Expense summary
                col1, col2, col3 = st.columns(3)
                
                deductible = expenses_df[expenses_df['tax_deductible'] == True]['amount'].sum()
                non_deductible = total_expenses - deductible
                
                with col1:
                    st.metric("Total Expenses", f"${total_expenses:,.2f}")
                with col2:
                    st.metric("Tax Deductible", f"${deductible:,.2f}", f"{(deductible/total_expenses*100):.0f}%")
                with col3:
                    st.metric("This Month", f"${expenses_df['amount'].head(10).sum():,.2f}")
                
                # Expense by category
                st.markdown("#### 💳 Expenses by Category")
                category_totals = expenses_df.groupby('category')['amount'].sum().to_dict()
                render_expense_category_chart(category_totals)
                
                # Recent expenses
                st.markdown("#### 📜 Recent Expenses")
                st.dataframe(
                    expenses_df.head(10)[['date', 'merchant', 'amount', 'category', 'tax_deductible']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Tax deduction tips
                st.markdown("---")
                st.markdown("#### 💡 Tax Deduction Tips")
                tips = TaxManager.get_deduction_tips(expenses_df)
                for tip in tips:
                    st.info(tip)
            else:
                st.info("No expenses tracked yet")
    
    # NEW CASH FLOW TAB (tab6)
    if NEW_FEATURES_AVAILABLE:
        with tab6:
            st.markdown("### 📈 Cash Flow Forecasting")
            
            # Generate forecast
            income_history = st.session_state.get('transactions_df', pd.DataFrame()).query('transaction_type == "credit"')
            expense_history = st.session_state.get('expenses_df', pd.DataFrame())
            invoices_df = st.session_state.get('invoices_df', pd.DataFrame())
            outstanding_invoices = invoices_df[invoices_df['status'] != 'paid'].to_dict('records') if not invoices_df.empty else []
            
            forecast = CashFlowEngine.forecast_cash_flow(
                income_history=income_history,
                expense_history=expense_history,
                outstanding_invoices=outstanding_invoices,
                forecast_days=90
            )
            
            # Display forecast
            render_cash_flow_forecast(forecast)
            
            st.markdown("---")
            
            # Financial metrics
            col1, col2, col3 = st.columns(3)
            
            current_balance = st.session_state.get('bank_account', {}).get('balance', 25000)
            monthly_expenses = forecast['summary']['avg_monthly_expenses']
            monthly_income = forecast['summary']['avg_monthly_income']
            
            runway = CashFlowEngine.calculate_runway(
                current_balance=current_balance,
                monthly_burn_rate=monthly_expenses,
                monthly_income=monthly_income
            )
            
            with col1:
                st.metric("Current Balance", f"${current_balance:,.0f}")
            with col2:
                st.metric("Monthly Net", f"${monthly_income - monthly_expenses:,.0f}", 
                         f"${monthly_income:,.0f} in, ${monthly_expenses:,.0f} out")
            with col3:
                if runway['runway_months'] < float('inf'):
                    st.metric("Runway", f"{runway['runway_months']:.1f} months", runway['status'])
                else:
                    st.metric("Cash Flow", "Positive ✅", "Sustainable")
            
            # Insights
            st.markdown("---")
            st.markdown("### 💡 Cash Flow Insights")
            
            st.info(runway['message'])
            st.success(f"📊 {forecast['summary']['forecast_accuracy']} forecast accuracy")
            
            if runway['runway_months'] < 6 and runway['runway_months'] != float('inf'):
                st.warning(f"⚠️ {runway['recommendation']}")
    
    # TRADING & PORTFOLIO TAB (tab7 - was tab4)
    # This preserves the existing trading functionality
    tab_to_use = tab7 if NEW_FEATURES_AVAILABLE else tab4
    with tab_to_use:
        st.markdown("### 📊 Trading & Portfolio")
        
        # Portfolio Section
        st.markdown("#### Your Investment Portfolio")
        
        # Get data source preference
        use_live = st.session_state.get('use_live_data', False)
        
        # Show data source indicator
        if use_live and LIVE_DATA_AVAILABLE:
            st.caption("📡 Using live portfolio prices (5min cache)")
        else:
            st.caption("📊 Using demo portfolio data")
        
        portfolio_df = generate_portfolio_data(use_live=use_live)
        total_value = portfolio_df['market_value'].sum()
        total_cost = portfolio_df['cost_basis'].sum()
        total_gain = total_value - total_cost
        total_gain_pct = (total_gain / total_cost) * 100
        
        # Portfolio summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value", f"${total_value:,.2f}")
        with col2:
            st.metric("Total Cost", f"${total_cost:,.2f}")
        with col3:
            st.metric("Total Gain/Loss", f"${total_gain:,.2f}", f"{total_gain_pct:+.2f}%")
        with col4:
            st.metric("Cash Balance", "$12,450.00")
        
        st.markdown("---")
        
        # Portfolio breakdown
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Holdings")
            st.dataframe(
                portfolio_df[[
                    'symbol', 'shares', 'avg_price', 'current_price', 
                    'market_value', 'gain_loss', 'gain_loss_pct'
                ]].style.format({
                    'avg_price': '${:.2f}',
                    'current_price': '${:.2f}',
                    'market_value': '${:,.2f}',
                    'gain_loss': '${:,.2f}',
                    'gain_loss_pct': '{:+.2f}%'
                }),
                width='stretch',
                hide_index=True
            )
        
        with col2:
            st.markdown("##### Allocation")
            pie_chart = create_portfolio_pie(portfolio_df)
            st.plotly_chart(pie_chart, use_container_width=True, key='portfolio_pie')
        
        # Performance chart
        st.markdown("##### 📈 Portfolio Performance (30 Days)")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        performance = total_cost * (1 + np.random.normal(0.001, 0.02, 30)).cumprod()
        
        perf_df = pd.DataFrame({
            'Date': dates,
            'Portfolio Value': performance
        })
        
        fig = px.line(
            perf_df, 
            x='Date', 
            y='Portfolio Value',
            title='Portfolio Growth'
        )
        fig.update_traces(line_color='#1D6F7A', line_width=3)
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True, key='perf_chart')
    
    # AI ASSISTANT TAB (tab8 - was tab3)  
    # Enhanced with business, trading, and emotion context
    tab_to_use_ai = tab8 if NEW_FEATURES_AVAILABLE else tab3
    with tab_to_use_ai:
        st.markdown("### 🤖 AI Financial Assistant")
        
        if NEW_FEATURES_AVAILABLE:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(29, 111, 122, 0.1) 100%); 
                        padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 4px solid #3B82F6;
                        animation: fadeIn 0.6s ease-out;">
                <h4 style="color: #1D6F7A; margin-top: 0; font-size: 1.5rem;">💬 Your Complete Financial Advisor</h4>
                <p style="margin-bottom: 0; color: #4A5568; font-size: 1.05rem; line-height: 1.7;">
                    Get personalized advice that considers your <strong>emotional state</strong>, 
                    <strong>business cash flow</strong>, <strong>tax obligations</strong>, and <strong>investment portfolio</strong>. 
                    Ask about invoicing, taxes, trading, or any financial decision!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(29, 111, 122, 0.1) 100%); 
                        padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 4px solid #3B82F6;
                        animation: fadeIn 0.6s ease-out;">
                <h4 style="color: #1D6F7A; margin-top: 0; font-size: 1.5rem;">💬 Your Personal Trading Advisor</h4>
                <p style="margin-bottom: 0; color: #4A5568; font-size: 1.05rem; line-height: 1.7;">
                    Powered by local Ollama AI, get personalized trading advice that considers your <strong>emotional state</strong>, 
                    <strong>portfolio performance</strong>, and <strong>market conditions</strong>. Ask anything about trading strategies, 
                    technical analysis, or risk management!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            welcome_msg = "👋 Hi! I'm your PulseTrade AI Assistant. I can help you with business management, tax strategies, trading decisions, and emotional guidance. What would you like to know?" if NEW_FEATURES_AVAILABLE else "👋 Hi! I'm your PulseTrade AI Assistant. I can help you with trading strategies, market analysis, and emotional trading guidance. What would you like to know?"
            st.session_state.chat_history = [{'role': 'assistant', 'content': welcome_msg}]
        
        # Display chat history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>You:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <strong>🤖 AI Assistant:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        st.markdown("---")
        
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me anything...",
                placeholder="e.g., Should I invest my invoice payment or save for taxes?",
                key="chat_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send 📤", use_container_width=True, type="primary")
        
        if send_button and user_input:
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            # Enhanced context for business + trading
            if NEW_FEATURES_AVAILABLE:
                bank_balance = st.session_state.get('bank_account', {}).get('balance', 25000)
                tax_balance = st.session_state.get('tax_pot', {}).get('balance', 8500)
                outstanding = st.session_state.get('invoices_df', pd.DataFrame()).query('status != "paid"')['total'].sum() if not st.session_state.get('invoices_df', pd.DataFrame()).empty else 0
                
                context = f"""You are a professional financial advisor for PulseTrade, a comprehensive financial platform for freelancers.

Current user financial context:
- Emotional state: Calm (72%) - Optimal for decision-making
- Business account: ${bank_balance:,.0f}
- Tax savings pot: ${tax_balance:,.0f}
- Outstanding invoices: ${outstanding:,.0f}
- Investment portfolio: $68,450 (+5.2% today)
- Recent alert: Prevented panic sell, saved $450

User question: {user_input}

Provide helpful, concise advice (2-4 sentences) considering their complete financial picture and emotional state."""
            else:
                context = f"""You are a professional trading advisor for PulseTrade.
User emotional state: Calm (72%)
User question: {user_input}
Provide helpful, concise advice (2-3 sentences)."""
            
            with st.spinner("🤔 Thinking..."):
                ai_response = query_ollama(context)
            
            st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response})
            st.rerun()
        
        # Suggested questions
        st.markdown("---")
        st.markdown("### 💡 Suggested Questions")
        
        if NEW_FEATURES_AVAILABLE:
            suggestions = [
                "Should I pay estimated taxes now?",
                "When to follow up on overdue invoices?",
                "Can I afford to hire a contractor?",
                "Should I invest surplus cash?",
                "How to optimize my tax deductions?",
                "Best time to make trades?"
            ]
        else:
            suggestions = [
                "Should I trade when anxious?",
                "How to set stop losses?",
                "Best time to buy stocks?",
                "What's RSI indicator?",
                "How to manage risk?",
                "Portfolio diversification tips?"
            ]
        
        col1, col2, col3 = st.columns(3)
        for idx, suggestion in enumerate(suggestions[:3]):
            with [col1, col2, col3][idx]:
                if st.button(f"💬 {suggestion}", key=f"sug_{idx}", use_container_width=True):
                    st.session_state.chat_history.append({'role': 'user', 'content': suggestion})
                    context = f"""You are a professional financial advisor for PulseTrade.
User question: {suggestion}
Provide helpful, concise advice."""
                    ai_response = query_ollama(context)
                    st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response})
                    st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            welcome_msg = "👋 Hi! I'm your PulseTrade AI Assistant. What would you like to know?"
            st.session_state.chat_history = [{'role': 'assistant', 'content': welcome_msg}]
            st.rerun()
    
    # COMMUNITY TAB (tab9 - was tab5)
    tab_to_use_community = tab9 if NEW_FEATURES_AVAILABLE else tab5
    with tab_to_use_community:
        st.markdown("### 👥 Community Feed")
        
        if NEW_FEATURES_AVAILABLE:
            st.info("💡 Share both trading insights AND freelance tips! Connect with traders and freelancers worldwide.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Post creation
            with st.expander("✍️ Create a Post", expanded=False):
                post_content = st.text_area("Share your insights...", placeholder="What are you working on today?")
                post_ticker = st.text_input("Topic/Ticker (optional)", placeholder="e.g., AAPL or #FreelanceTips")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    post_signal = st.selectbox("Signal/Type", ["BUY", "SELL", "HOLD", "TIP", "QUESTION"])
                with col_b:
                    if st.button("📤 Post", type="primary", key="post_btn"):
                        st.success("Post shared with community!")
                with col_c:
                    if st.button("📷 Add Chart", key="chart_btn"):
                        st.info("Chart upload coming soon!")
            
            # Community posts
            st.markdown("#### Recent Community Posts")
            
            posts = generate_community_posts()
            
            for post in posts[:5]:
                signal_class = f"signal-{post['signal'].lower()}"
                
                st.markdown(f"""
                <div class="community-post">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div>
                            <strong>{post['user']}</strong>
                            <span class="user-badge">VERIFIED</span>
                        </div>
                        <small style="color: #626C71;">{post['timestamp'].strftime('%I:%M %p')}</small>
                    </div>
                    <p style="margin: 0.5rem 0;">{post['content']}</p>
                    <div style="margin-top: 0.5rem;">
                        <span class="trade-signal {signal_class}">${post['ticker']} - {post['signal']}</span>
                    </div>
                    <div style="margin-top: 0.75rem; color: #626C71; font-size: 0.9rem;">
                        <span style="margin-right: 1rem;">❤️ {post['likes']}</span>
                        <span>💬 {post['comments']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
        
        with col2:
            st.markdown("#### 🏆 Top Contributors")
            
            traders = pd.DataFrame({
                'User': ['Mike_Investor', 'Emma_Finance', 'Sarah_Trader', 'Alex_Markets', 'Jordan_Tech'],
                'Performance': ['+15.2%', '+12.8%', '+11.3%', '+9.7%', '+8.5%'],
                'Followers': ['2.4K', '1.8K', '1.5K', '1.2K', '950']
            })
            
            for idx, row in traders.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.75rem 0; border: 2px solid #E1E8EB; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #0F2B33; font-size: 1rem;">{row['User']}</div>
                    <div style="color: #059669; font-size: 1.25rem; font-weight: 700; margin: 0.25rem 0;">{row['Performance']}</div>
                    <div style="color: #4A5F66; font-size: 0.875rem; font-weight: 500;">{row['Followers']} followers</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("#### 💡 Trending Topics")
            topics = ['#TechEarnings', '#FreelanceTips', '#TaxStrategy', '#InvoicingHacks', '#MarketRally']
            for topic in topics:
                st.markdown(f"**{topic}** • 523 posts")
    
    # LEARN TAB (tab10 - was tab6)
    tab_to_use_learn = tab10 if NEW_FEATURES_AVAILABLE else tab6
    with tab_to_use_learn:
        st.markdown("### 🎓 Learning Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📚 Featured Courses")
            
            if NEW_FEATURES_AVAILABLE:
                courses = [
                    {'title': 'Freelance Finance Fundamentals', 'duration': '1 hour', 'level': 'Beginner', 'students': '3,245'},
                    {'title': 'Tax Strategies for Freelancers', 'duration': '2 hours', 'level': 'Intermediate', 'students': '2,892'},
                    {'title': 'Cash Flow Management Mastery', 'duration': '1.5 hours', 'level': 'Intermediate', 'students': '1,834'},
                    {'title': 'Investment Portfolio Building', 'duration': '2.5 hours', 'level': 'Advanced', 'students': '1,234'}
                ]
            else:
                courses = [
                    {'title': 'Technical Analysis Fundamentals', 'duration': '45 mins', 'level': 'Beginner', 'students': '2,345'},
                    {'title': 'Options Trading Strategies', 'duration': '2 hours', 'level': 'Intermediate', 'students': '1,892'},
                    {'title': 'Portfolio Risk Management', 'duration': '1.5 hours', 'level': 'Advanced', 'students': '1,234'}
                ]
            
            for course in courses:
                with st.container():
                    st.markdown(f"""
                    <div style="background: white; padding: 1.75rem; border-radius: 12px; margin: 1rem 0; border: 2px solid #E1E8EB; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <h4 style="color: #1D6F7A; margin: 0 0 0.75rem 0; font-size: 1.25rem; font-weight: 700;">{course['title']}</h4>
                        <div style="color: #4A5F66; font-size: 0.95rem; font-weight: 500;">
                            <span>⏱️ {course['duration']}</span> • 
                            <span>📊 {course['level']}</span> • 
                            <span>👥 {course['students']} students</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Start Course →", key=f"course_{course['title']}", type="primary"):
                        st.success(f"Starting '{course['title']}'...")
        
        with col2:
            st.markdown("#### 📖 Latest Articles")
            
            if NEW_FEATURES_AVAILABLE:
                articles = [
                    "Complete Guide to Quarterly Tax Estimates",
                    "Invoicing Best Practices for Freelancers",
                    "Building Emergency Funds on Irregular Income",
                    "Investment Strategies for Self-Employed"
                ]
            else:
                articles = [
                    "Understanding Market Volatility in 2024",
                    "Top 5 Technical Indicators Every Trader Should Know",
                    "Building a Balanced Portfolio: A Step-by-Step Guide",
                    "The Psychology of Trading: Avoiding Common Mistakes"
                ]
            
            for article in articles:
                st.markdown(f"""
                <div style="background: #F8F9FA; padding: 1.25rem; border-radius: 10px; margin: 0.75rem 0; border: 2px solid #E1E8EB;">
                    <div style="font-weight: 700; color: #0F2B33; font-size: 1rem; line-height: 1.4;">{article}</div>
                    <div style="color: #4A5F66; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 500;">
                        📖 5 min read • Published today
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("#### 🎥 Video Tutorials")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.markdown("**Cash Flow Forecasting Basics**" if NEW_FEATURES_AVAILABLE else "**How to Read Candlestick Charts**")
        
        with col2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.markdown("**Tax Deductions You're Missing**" if NEW_FEATURES_AVAILABLE else "**Understanding Support & Resistance**")
        
        with col3:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.markdown("**Invoice Collection Strategies**" if NEW_FEATURES_AVAILABLE else "**Risk Management Basics**")
    
    # Original tab3 content (fallback for old version)
    if not NEW_FEATURES_AVAILABLE:
        with tab3:
            st.markdown("### 🤖 AI Trading Assistant")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(29, 111, 122, 0.1) 100%); 
                    padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 4px solid #3B82F6;
                    animation: fadeIn 0.6s ease-out;">
            <h4 style="color: #1D6F7A; margin-top: 0; font-size: 1.5rem;">💬 Your Personal Trading Advisor</h4>
            <p style="margin-bottom: 0; color: #4A5568; font-size: 1.05rem; line-height: 1.7;">
                Powered by local Ollama AI, get personalized trading advice that considers your <strong>emotional state</strong>, 
                <strong>portfolio performance</strong>, and <strong>market conditions</strong>. Ask anything about trading strategies, 
                technical analysis, or risk management!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [
                {
                    'role': 'assistant',
                    'content': "👋 Hi! I'm your PulseTrade AI Assistant. I can help you with trading strategies, market analysis, and emotional trading guidance. What would you like to know?"
                }
            ]
        
        # Display chat history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>You:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <strong>🤖 AI Assistant:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        st.markdown("---")
        
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me anything about trading...",
                placeholder="e.g., Should I trade when I'm feeling anxious?",
                key="chat_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send 📤", use_container_width=True, type="primary")
        
        if send_button and user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Create context-aware prompt
            context = f"""You are a professional trading advisor for PulseTrade, a platform that monitors traders' emotions in real-time.
            
Current user context:
- Emotional state: Calm (72%)
- Current portfolio: $68,450 (+5.2% today)
- Recent alert: Prevented panic sell on TSLA, saved $450
- Win rate when calm: 72%

User question: {user_input}

Provide helpful, concise advice (2-3 sentences) considering their emotional state and trading psychology. Be supportive and data-driven."""
            
            # Query Ollama with animated loading
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="display: inline-flex; gap: 8px;">
                    <span class="ai-dot" style="width: 12px; height: 12px; background: #1D6F7A; border-radius: 50%; display: inline-block;"></span>
                    <span class="ai-dot" style="width: 12px; height: 12px; background: #1D6F7A; border-radius: 50%; display: inline-block;"></span>
                    <span class="ai-dot" style="width: 12px; height: 12px; background: #1D6F7A; border-radius: 50%; display: inline-block;"></span>
                </div>
                <p class="ai-thinking" style="margin-top: 0.5rem; color: #4A5568;">AI thinking...</p>
            </div>
            """, unsafe_allow_html=True)
            
            ai_response = query_ollama(context)
            
            # Add AI response
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response
            })
            
            st.rerun()
        
        # Suggested questions
        st.markdown("---")
        st.markdown("### 💡 Suggested Questions")
        
        col1, col2, col3 = st.columns(3)
        
        suggestions = [
            "Should I trade when anxious?",
            "How to set stop losses?",
            "Best time to buy stocks?",
            "What's RSI indicator?",
            "How to manage risk?",
            "Portfolio diversification tips?"
        ]
        
        for idx, suggestion in enumerate(suggestions[:3]):
            with col1 if idx == 0 else col2 if idx == 1 else col3:
                if st.button(f"💬 {suggestion}", key=f"sug_{idx}", use_container_width=True):
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': suggestion
                    })
                    
                    context = f"""You are a professional trading advisor for PulseTrade.
User emotional state: Calm (72%)
User question: {suggestion}
Provide helpful, concise advice (2-3 sentences)."""
                    
                    ai_response = query_ollama(context)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': ai_response
                    })
                    
                    st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.chat_history = [
                {
                    'role': 'assistant',
                    'content': "👋 Hi! I'm your PulseTrade AI Assistant. I can help you with trading strategies, market analysis, and emotional trading guidance. What would you like to know?"
                }
            ]
            st.rerun()
    
    with tab4:
        st.markdown("### 💼 Portfolio & Market Analysis")
        
        # Portfolio Section
        st.markdown("#### Your Portfolio")
        
        # Get data source preference
        use_live = st.session_state.get('use_live_data', False)
        
        # Show data source indicator
        if use_live and LIVE_DATA_AVAILABLE:
            st.caption("📡 Using live portfolio prices (5min cache)")
        else:
            st.caption("📊 Using demo portfolio data")
        
        portfolio_df = generate_portfolio_data(use_live=use_live)
        total_value = portfolio_df['market_value'].sum()
        total_cost = portfolio_df['cost_basis'].sum()
        total_gain = total_value - total_cost
        total_gain_pct = (total_gain / total_cost) * 100
        
        # Portfolio summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value", f"${total_value:,.2f}")
        with col2:
            st.metric("Total Cost", f"${total_cost:,.2f}")
        with col3:
            st.metric("Total Gain/Loss", f"${total_gain:,.2f}", f"{total_gain_pct:+.2f}%")
        with col4:
            st.metric("Cash Balance", "$12,450.00")
        
        st.markdown("---")
        
        # Portfolio breakdown
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Holdings")
            st.dataframe(
                portfolio_df[[
                    'symbol', 'shares', 'avg_price', 'current_price', 
                    'market_value', 'gain_loss', 'gain_loss_pct'
                ]].style.format({
                    'avg_price': '${:.2f}',
                    'current_price': '${:.2f}',
                    'market_value': '${:,.2f}',
                    'gain_loss': '${:,.2f}',
                    'gain_loss_pct': '{:+.2f}%'
                }),
                width='stretch',
                hide_index=True
            )
        
        with col2:
            st.markdown("##### Allocation")
            pie_chart = create_portfolio_pie(portfolio_df)
            st.plotly_chart(pie_chart, use_container_width=True, key='portfolio_pie')
        
        # Performance chart
        st.markdown("##### 📈 Portfolio Performance (30 Days)")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        performance = total_cost * (1 + np.random.normal(0.001, 0.02, 30)).cumprod()
        
        perf_df = pd.DataFrame({
            'Date': dates,
            'Portfolio Value': performance
        })
        
        fig = px.line(
            perf_df, 
            x='Date', 
            y='Portfolio Value',
            title='Portfolio Growth'
        )
        fig.update_traces(line_color='#1D6F7A', line_width=3)
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True, key='perf_chart')
        
        st.markdown("---")
        
        # Market Analysis Section
        st.markdown("#### Market Analysis Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Sector Performance")
            sectors_df = pd.DataFrame({
                'Sector': ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer', 'Industrials'],
                'Change': [2.3, 1.1, -0.5, -1.2, 0.8, 1.5]
            })
            
            fig = px.bar(
                sectors_df, 
                x='Sector', 
                y='Change',
                color='Change',
                color_continuous_scale=['red', 'yellow', 'green'],
                title='Sector Performance Today'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key='sector_chart')
        
        with col2:
            st.markdown("#### 📊 Market Breadth")
            
            breadth_data = {
                'Advancing': 1845,
                'Declining': 1234,
                'Unchanged': 156
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(breadth_data.keys()),
                values=list(breadth_data.values()),
                marker_colors=['#22c55e', '#ef4444', '#6b7280']
            )])
            fig.update_layout(height=350, title='NYSE Advance/Decline')
            st.plotly_chart(fig, use_container_width=True, key='breadth_chart')
        
        # Economic Calendar
        st.markdown("#### 📅 Economic Calendar")
        
        calendar_df = pd.DataFrame({
            'Date': ['Oct 10', 'Oct 11', 'Oct 12', 'Oct 13', 'Oct 14'],
            'Time': ['8:30 AM', '2:00 PM', '8:30 AM', '10:00 AM', 'All Day'],
            'Event': ['CPI Data', 'Fed Minutes', 'Jobless Claims', 'Consumer Sentiment', 'Earnings Season'],
            'Impact': ['🔴 High', '🟡 Medium', '🟡 Medium', '🟢 Low', '🔴 High']
        })
        
        st.dataframe(calendar_df, width='stretch', hide_index=True)
        
        # Screener
        st.markdown("#### 🔍 Stock Screener")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            min_price = st.number_input("Min Price ($)", value=0.0)
        with col2:
            max_price = st.number_input("Max Price ($)", value=1000.0)
        with col3:
            min_volume = st.number_input("Min Volume (M)", value=0.0)
        
        if st.button("🔍 Run Screener", type="primary"):
            st.success("Found 47 stocks matching your criteria!")
            
            screener_results = pd.DataFrame({
                'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META'],
                'Price': [178.32, 385.20, 142.15, 502.40, 312.85],
                'Volume': ['52.3M', '24.1M', '18.5M', '38.7M', '15.2M'],
                'P/E': [28.5, 35.2, 24.8, 72.3, 29.1],
                'Signal': ['🟢 BUY', '🟡 HOLD', '🟢 BUY', '🟢 BUY', '🟡 HOLD']
            })
            
            st.dataframe(screener_results, width='stretch', hide_index=True)
    
    with tab5:
        st.markdown("### Community Feed")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Post creation
            with st.expander("✍️ Create a Post", expanded=False):
                post_content = st.text_area("Share your insights...", placeholder="What are you trading today?")
                post_ticker = st.text_input("Ticker (optional)", placeholder="e.g., AAPL")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    post_signal = st.selectbox("Signal", ["BUY", "SELL", "HOLD"])
                with col_b:
                    if st.button("📤 Post", type="primary"):
                        st.success("Post shared with community!")
                with col_c:
                    if st.button("📷 Add Chart"):
                        st.info("Chart upload coming soon!")
            
            # Community posts
            st.markdown("#### Recent Community Posts")
            
            posts = generate_community_posts()
            
            for post in posts[:5]:
                signal_class = f"signal-{post['signal'].lower()}"
                
                st.markdown(f"""
                <div class="community-post">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div>
                            <strong>{post['user']}</strong>
                            <span class="user-badge">VERIFIED</span>
                        </div>
                        <small style="color: #626C71;">{post['timestamp'].strftime('%I:%M %p')}</small>
                    </div>
                    <p style="margin: 0.5rem 0;">{post['content']}</p>
                    <div style="margin-top: 0.5rem;">
                        <span class="trade-signal {signal_class}">${post['ticker']} - {post['signal']}</span>
                    </div>
                    <div style="margin-top: 0.75rem; color: #626C71; font-size: 0.9rem;">
                        <span style="margin-right: 1rem;">❤️ {post['likes']}</span>
                        <span>💬 {post['comments']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
        
        with col2:
            st.markdown("#### 🏆 Top Traders This Week")
            
            traders = pd.DataFrame({
                'Trader': ['Mike_Investor', 'Emma_Finance', 'Sarah_Trader', 'Alex_Markets', 'Jordan_Tech'],
                'Gain': ['+15.2%', '+12.8%', '+11.3%', '+9.7%', '+8.5%'],
                'Followers': ['2.4K', '1.8K', '1.5K', '1.2K', '950']
            })
            
            for idx, row in traders.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.75rem 0; border: 2px solid #E1E8EB; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #0F2B33; font-size: 1rem;">{row['Trader']}</div>
                    <div style="color: #059669; font-size: 1.25rem; font-weight: 700; margin: 0.25rem 0;">{row['Gain']}</div>
                    <div style="color: #4A5F66; font-size: 0.875rem; font-weight: 500;">{row['Followers']} followers</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("#### 💡 Trending Topics")
            topics = ['#TechEarnings', '#FedMinutes', '#MarketRally', '#OptionsTrading', '#DividendStocks']
            for topic in topics:
                st.markdown(f"**{topic}** • 523 posts")
    
    with tab6:
        st.markdown("### Learning Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📚 Featured Courses")
            
            courses = [
                {
                    'title': 'Technical Analysis Fundamentals',
                    'duration': '45 mins',
                    'level': 'Beginner',
                    'students': '2,345'
                },
                {
                    'title': 'Options Trading Strategies',
                    'duration': '2 hours',
                    'level': 'Intermediate',
                    'students': '1,892'
                },
                {
                    'title': 'Portfolio Risk Management',
                    'duration': '1.5 hours',
                    'level': 'Advanced',
                    'students': '1,234'
                }
            ]
            
            for course in courses:
                with st.container():
                    st.markdown(f"""
                    <div style="background: white; padding: 1.75rem; border-radius: 12px; margin: 1rem 0; border: 2px solid #E1E8EB; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <h4 style="color: #1D6F7A; margin: 0 0 0.75rem 0; font-size: 1.25rem; font-weight: 700;">{course['title']}</h4>
                        <div style="color: #4A5F66; font-size: 0.95rem; font-weight: 500;">
                            <span>⏱️ {course['duration']}</span> • 
                            <span>📊 {course['level']}</span> • 
                            <span>👥 {course['students']} students</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Start Course →", key=f"course_{course['title']}", type="primary"):
                        st.success(f"Starting '{course['title']}'...")
        
        with col2:
            st.markdown("#### 📖 Latest Articles")
            
            articles = [
                "Understanding Market Volatility in 2024",
                "Top 5 Technical Indicators Every Trader Should Know",
                "Building a Balanced Portfolio: A Step-by-Step Guide",
                "The Psychology of Trading: Avoiding Common Mistakes"
            ]
            
            for article in articles:
                st.markdown(f"""
                <div style="background: #F8F9FA; padding: 1.25rem; border-radius: 10px; margin: 0.75rem 0; border: 2px solid #E1E8EB;">
                    <div style="font-weight: 700; color: #0F2B33; font-size: 1rem; line-height: 1.4;">{article}</div>
                    <div style="color: #4A5F66; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 500;">
                        📖 5 min read • Published today
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("#### 🎥 Video Tutorials")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.markdown("**How to Read Candlestick Charts**")
        
        with col2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.markdown("**Understanding Support & Resistance**")
        
        with col3:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.markdown("**Risk Management Basics**")

# Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #4A5F66; padding: 2.5rem 0; background: #F8F9FA; border-radius: 12px; margin-top: 2rem;">
        <p style="font-size: 1.25rem; font-weight: 700; color: #1D6F7A; margin-bottom: 0.5rem;">PulseTrade</p>
        <p style="font-weight: 600; margin-bottom: 1rem;">""" + (
            "The Complete Financial OS for Freelancers" if NEW_FEATURES_AVAILABLE else 
            "Empowering Retail Investors Through Data + Community"
        ) + """</p>
        <p style="font-size: 0.875rem; color: #6B7280;">Demo Version • All data is synthetic for demonstration purposes</p>
        <p style="font-size: 0.875rem; color: #6B7280;">© 2025 PulseTrade. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

