"""
Application Enhancements Module
Patches and optimizations for demo_app.py without modifying the main file

Usage: Import this in demo_app.py to enable all enhancements
"""

import streamlit as st
from functools import wraps
import time
from typing import Callable, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def track_time(self, operation_name: str):
        """Decorator to track operation time"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                
                self.metrics[operation_name] = elapsed_time
                
                if elapsed_time > 1.0:  # Log slow operations
                    logger.warning(f"{operation_name} took {elapsed_time:.2f}s")
                
                return result
            return wrapper
        return decorator
    
    def get_metrics(self):
        """Get all performance metrics"""
        return self.metrics


class CacheManager:
    """Manage application-level caching"""
    
    @staticmethod
    def clear_all_caches():
        """Clear all Streamlit caches"""
        st.cache_data.clear()
        logger.info("All caches cleared")
    
    @staticmethod
    def get_cache_stats():
        """Get cache statistics"""
        # Streamlit doesn't expose cache stats directly
        # This is a placeholder for future implementation
        return {
            "status": "Cache management active",
            "auto_clear": False
        }


class ErrorBoundary:
    """Application-wide error handling"""
    
    @staticmethod
    def wrap(func: Callable, error_message: str = "An error occurred") -> Callable:
        """Wrap function with error boundary"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{error_message}: {str(e)}", exc_info=True)
                st.error(f"""
                **{error_message}**
                
                {str(e)}
                
                Please try refreshing the page or contact support if the issue persists.
                """)
                
                # In debug mode, show full traceback
                if st.session_state.get('debug_mode', False):
                    st.exception(e)
                
                return None
        return wrapper


class AccessibilityEnhancements:
    """Accessibility improvements"""
    
    @staticmethod
    def add_aria_labels():
        """Add ARIA labels to components"""
        st.markdown("""
        <script>
        // Add ARIA labels to Streamlit components
        document.addEventListener('DOMContentLoaded', function() {
            // Label buttons
            document.querySelectorAll('button').forEach((btn, index) => {
                if (!btn.getAttribute('aria-label')) {
                    btn.setAttribute('aria-label', btn.textContent || `Button ${index + 1}`);
                }
            });
            
            // Label inputs
            document.querySelectorAll('input').forEach((input, index) => {
                if (!input.getAttribute('aria-label')) {
                    input.setAttribute('aria-label', input.placeholder || `Input ${index + 1}`);
                }
            });
        });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_skip_navigation():
        """Add skip to main content link"""
        st.markdown("""
        <a href="#main-content" class="skip-link" 
           style="position: absolute; left: -9999px; z-index: 999;">
            Skip to main content
        </a>
        <style>
        .skip-link:focus {
            left: 0;
            top: 0;
            background: #1D6F7A;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 0 0 4px 0;
        }
        </style>
        <div id="main-content" role="main"></div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_keyboard_navigation_hints():
        """Add keyboard navigation instructions"""
        with st.expander("⌨️ Keyboard Navigation", expanded=False):
            st.markdown("""
            **Keyboard Shortcuts:**
            - `Tab` - Navigate between elements
            - `Shift + Tab` - Navigate backwards
            - `Enter` - Activate buttons and links
            - `Space` - Toggle checkboxes and buttons
            - `Esc` - Close modals and dropdowns
            - `Arrow keys` - Navigate within components
            """)


class PerformanceOptimizations:
    """Performance optimization utilities"""
    
    @staticmethod
    def optimize_dataframe(df, max_rows: int = 1000):
        """Optimize DataFrame for display"""
        if df is None or len(df) == 0:
            return df
        
        if len(df) > max_rows:
            # Sample intelligently
            step = len(df) // max_rows
            return df.iloc[::step]
        
        return df
    
    @staticmethod
    def lazy_load_images():
        """Enable lazy loading for images"""
        st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('img').forEach(img => {
                img.setAttribute('loading', 'lazy');
            });
        });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_performance_hints():
        """Add performance meta tags"""
        st.markdown("""
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
        <meta name="theme-color" content="#1D6F7A">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        """, unsafe_allow_html=True)


class ConsistencyEnforcer:
    """Ensure UI consistency across the app"""
    
    @staticmethod
    def apply_consistent_styling():
        """Apply consistent styling"""
        st.markdown("""
        <style>
        /* Ensure all buttons have consistent styling */
        .stButton > button {
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        /* Consistent card styling */
        .element-container {
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Consistent spacing */
        .stMarkdown {
            margin-bottom: 1rem;
        }
        
        /* Consistent table styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Ensure consistent heights for metric cards */
        [data-testid="stMetric"] {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #E5E7EB;
            height: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def standardize_colors():
        """Standardize color usage"""
        return {
            'primary': '#1D6F7A',
            'primary_light': '#2AA5B3',
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'info': '#3B82F6',
        }


def initialize_enhancements():
    """
    Initialize all enhancements
    Call this at the start of your Streamlit app
    """
    # Apply accessibility enhancements
    AccessibilityEnhancements.add_skip_navigation()
    AccessibilityEnhancements.add_aria_labels()
    
    # Apply performance optimizations
    PerformanceOptimizations.add_performance_hints()
    PerformanceOptimizations.lazy_load_images()
    
    # Apply consistency
    ConsistencyEnforcer.apply_consistent_styling()
    
    # Initialize session state for debug mode
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    
    # Initialize performance monitor
    if 'perf_monitor' not in st.session_state:
        st.session_state.perf_monitor = PerformanceMonitor()
    
    logger.info("All enhancements initialized")


def add_debug_panel():
    """Add debug panel in sidebar (only shown if debug mode is enabled)"""
    if st.session_state.get('debug_mode', False):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🐛 Debug Panel")
            
            if st.button("Clear All Caches"):
                CacheManager.clear_all_caches()
                st.success("Caches cleared!")
            
            if st.button("Show Performance Metrics"):
                metrics = st.session_state.perf_monitor.get_metrics()
                st.json(metrics)
            
            if st.button("Show Session State"):
                # Filter out large objects
                safe_state = {k: str(v)[:100] for k, v in st.session_state.items()}
                st.json(safe_state)


def enable_debug_mode():
    """Enable debug mode (call with ?debug=true URL parameter)"""
    query_params = st.query_params
    if query_params.get('debug') == 'true':
        st.session_state.debug_mode = True
        logger.info("Debug mode enabled")


# Utility functions for common patterns
def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safe division with fallback"""
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def format_currency(amount: float, currency: str = "$") -> str:
    """Format currency consistently"""
    return f"{currency}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage consistently"""
    return f"{value:+.{decimals}f}%"


def format_large_number(num: float) -> str:
    """Format large numbers with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{num:.0f}"


# Export commonly used functions
__all__ = [
    'PerformanceMonitor',
    'CacheManager',
    'ErrorBoundary',
    'AccessibilityEnhancements',
    'PerformanceOptimizations',
    'ConsistencyEnforcer',
    'initialize_enhancements',
    'add_debug_panel',
    'enable_debug_mode',
    'safe_divide',
    'format_currency',
    'format_percentage',
    'format_large_number',
]

