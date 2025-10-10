"""
Utilities Module
Helper functions and configurations
"""

from .app_enhancements import (
    initialize_enhancements,
    enable_debug_mode,
    add_debug_panel,
    ErrorBoundary,
    format_currency,
    format_percentage
)

from .performance_config import (
    CACHE_TTL,
    UI_CONFIG,
    ACCESSIBILITY_CONFIG,
    CHART_COLORS,
    CHART_STYLES
)

from .validation import (
    ValidationError,
    InputValidator,
    DataValidator,
    SessionStateValidator,
    validate_and_show_error
)

from .seo_meta import (
    SEOManager,
    AccessibilityEnhancer,
    PerformanceOptimizer,
    initialize_seo_and_meta
)

__all__ = [
    # App Enhancements
    'initialize_enhancements',
    'enable_debug_mode',
    'add_debug_panel',
    'ErrorBoundary',
    'format_currency',
    'format_percentage',
    
    # Performance Config
    'CACHE_TTL',
    'UI_CONFIG',
    'ACCESSIBILITY_CONFIG',
    'CHART_COLORS',
    'CHART_STYLES',
    
    # Validation
    'ValidationError',
    'InputValidator',
    'DataValidator',
    'SessionStateValidator',
    'validate_and_show_error',
    
    # SEO & Meta
    'SEOManager',
    'AccessibilityEnhancer',
    'PerformanceOptimizer',
    'initialize_seo_and_meta'
]

