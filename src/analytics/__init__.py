"""
Analytics Module
Advanced analytics for trading, business, and unified financial insights
"""

# Trading analytics (existing)
from .analytics_engine import (
    EmotionAnalytics,
    PortfolioAnalytics,
    MarketInsights,
    generate_daily_insights,
    TradingSignal,
    EmotionalState,
    TradingInsight
)

# Cash flow and business analytics (new)
from .cashflow_engine import CashFlowEngine

# Unified insights (new)
from .unified_insights import UnifiedInsights

__all__ = [
    # Trading
    'EmotionAnalytics',
    'PortfolioAnalytics',
    'MarketInsights',
    'generate_daily_insights',
    'TradingSignal',
    'EmotionalState',
    'TradingInsight',
    # Business
    'CashFlowEngine',
    # Unified
    'UnifiedInsights'
]

