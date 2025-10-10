"""
Portfolio Management Module
Handles investment portfolio tracking, analysis, and insights
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class PortfolioHolding:
    """Represents a single portfolio holding"""
    symbol: str
    shares: float
    avg_price: float
    current_price: float
    
    @property
    def market_value(self) -> float:
        return self.shares * self.current_price
    
    @property
    def cost_basis(self) -> float:
        return self.shares * self.avg_price
    
    @property
    def gain_loss(self) -> float:
        return self.market_value - self.cost_basis
    
    @property
    def gain_loss_pct(self) -> float:
        if self.cost_basis == 0:
            return 0
        return (self.gain_loss / self.cost_basis) * 100


class PortfolioManager:
    """Manages investment portfolio with analytics and insights"""
    
    @staticmethod
    def create_holding(symbol: str, shares: float, avg_price: float, 
                      current_price: float) -> PortfolioHolding:
        """Create a portfolio holding"""
        return PortfolioHolding(
            symbol=symbol,
            shares=shares,
            avg_price=avg_price,
            current_price=current_price
        )
    
    @staticmethod
    def calculate_portfolio_metrics(holdings: List[PortfolioHolding]) -> Dict[str, Any]:
        """
        Calculate comprehensive portfolio metrics
        
        Args:
            holdings: List of PortfolioHolding objects
            
        Returns:
            dict: Portfolio metrics including total value, gain/loss, diversity score, etc.
        """
        if not holdings:
            return {
                'total_value': 0,
                'total_cost': 0,
                'total_gain_loss': 0,
                'total_gain_loss_pct': 0,
                'diversity_score': 0,
                'num_holdings': 0,
                'largest_position_pct': 0
            }
        
        total_value = sum(h.market_value for h in holdings)
        total_cost = sum(h.cost_basis for h in holdings)
        total_gain_loss = total_value - total_cost
        total_gain_loss_pct = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
        
        # Calculate diversity score (higher is better, max 100)
        # Based on: number of holdings, concentration risk, sector diversity
        num_holdings = len(holdings)
        
        # Calculate concentration (largest position as % of portfolio)
        if total_value > 0:
            position_percentages = [h.market_value / total_value * 100 for h in holdings]
            largest_position_pct = max(position_percentages)
            
            # Diversity score: penalize concentration, reward more holdings
            # Perfect score: 10+ holdings, no position > 15%
            holdings_score = min(num_holdings / 10 * 50, 50)  # Max 50 points
            concentration_score = max(0, (30 - largest_position_pct) / 30 * 50)  # Max 50 points
            diversity_score = holdings_score + concentration_score
        else:
            largest_position_pct = 0
            diversity_score = 0
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_pct': total_gain_loss_pct,
            'diversity_score': diversity_score,
            'num_holdings': num_holdings,
            'largest_position_pct': largest_position_pct
        }
    
    @staticmethod
    def get_top_performers(holdings: List[PortfolioHolding], top_n: int = 3) -> List[Dict[str, Any]]:
        """Get top performing holdings by gain %"""
        sorted_holdings = sorted(holdings, key=lambda h: h.gain_loss_pct, reverse=True)
        
        return [{
            'symbol': h.symbol,
            'gain_loss_pct': h.gain_loss_pct,
            'gain_loss': h.gain_loss,
            'market_value': h.market_value
        } for h in sorted_holdings[:top_n]]
    
    @staticmethod
    def get_bottom_performers(holdings: List[PortfolioHolding], bottom_n: int = 3) -> List[Dict[str, Any]]:
        """Get worst performing holdings by gain %"""
        sorted_holdings = sorted(holdings, key=lambda h: h.gain_loss_pct)
        
        return [{
            'symbol': h.symbol,
            'gain_loss_pct': h.gain_loss_pct,
            'gain_loss': h.gain_loss,
            'market_value': h.market_value
        } for h in sorted_holdings[:bottom_n]]
    
    @staticmethod
    def calculate_allocation(holdings: List[PortfolioHolding]) -> pd.DataFrame:
        """Calculate portfolio allocation by position"""
        total_value = sum(h.market_value for h in holdings)
        
        allocations = []
        for h in holdings:
            pct = (h.market_value / total_value * 100) if total_value > 0 else 0
            allocations.append({
                'symbol': h.symbol,
                'market_value': h.market_value,
                'allocation_pct': pct
            })
        
        return pd.DataFrame(allocations)
    
    @staticmethod
    def generate_rebalance_suggestions(holdings: List[PortfolioHolding], 
                                     target_allocation: Dict[str, float] = None) -> List[str]:
        """
        Generate rebalancing suggestions
        
        Args:
            holdings: List of PortfolioHolding objects
            target_allocation: Optional dict of symbol -> target % (e.g., {'AAPL': 20, 'GOOGL': 20})
            
        Returns:
            List of rebalancing suggestions as strings
        """
        suggestions = []
        total_value = sum(h.market_value for h in holdings)
        
        if total_value == 0:
            return ["Portfolio is empty. Start by adding positions."]
        
        # Check concentration risk
        for h in holdings:
            position_pct = (h.market_value / total_value * 100)
            if position_pct > 30:
                suggestions.append(
                    f"⚠️ {h.symbol} is {position_pct:.1f}% of portfolio. "
                    f"Consider reducing to under 30% for better diversification."
                )
        
        # Check number of holdings
        if len(holdings) < 5:
            suggestions.append(
                f"💡 Consider adding more holdings. You have {len(holdings)}, "
                f"ideal is 8-15 for good diversification."
            )
        elif len(holdings) > 20:
            suggestions.append(
                f"💡 You have {len(holdings)} holdings. Consider consolidating to "
                f"8-15 positions for easier management."
            )
        
        # Check target allocation if provided
        if target_allocation:
            for symbol, target_pct in target_allocation.items():
                holding = next((h for h in holdings if h.symbol == symbol), None)
                if holding:
                    actual_pct = (holding.market_value / total_value * 100)
                    diff = actual_pct - target_pct
                    
                    if abs(diff) > 5:  # More than 5% off target
                        action = "reduce" if diff > 0 else "increase"
                        suggestions.append(
                            f"🎯 {symbol}: Current {actual_pct:.1f}%, "
                            f"Target {target_pct:.1f}%. {action.capitalize()} position by "
                            f"${abs(diff/100 * total_value):.0f}."
                        )
        
        if not suggestions:
            suggestions.append("✅ Portfolio is well-balanced. No immediate rebalancing needed.")
        
        return suggestions
    
    @staticmethod
    def simulate_performance(holdings: List[PortfolioHolding], 
                           days: int = 30) -> pd.DataFrame:
        """
        Simulate historical portfolio performance
        
        Args:
            holdings: List of PortfolioHolding objects
            days: Number of days to simulate
            
        Returns:
            DataFrame with columns: date, portfolio_value
        """
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        total_cost = sum(h.cost_basis for h in holdings)
        
        # Simulate realistic returns (mean reversion around current performance)
        current_return = sum(h.gain_loss for h in holdings) / total_cost if total_cost > 0 else 0
        daily_returns = np.random.normal(current_return/days, 0.02, days)
        
        portfolio_values = total_cost * (1 + daily_returns).cumprod()
        
        return pd.DataFrame({
            'date': dates,
            'portfolio_value': portfolio_values
        })

