"""
Unified Insights Module
Combines business, trading, and emotion data for holistic financial view
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import streamlit as st

class UnifiedInsights:
    """Provides integrated insights across business, trading, and emotional intelligence"""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_total_net_worth(business_data: Dict[str, float],
                           trading_data: Dict[str, float],
                           personal_data: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Calculate total net worth across all accounts
        
        Args:
            business_data: Business accounts {'checking': X, 'tax_pot': Y, 'receivables': Z}
            trading_data: Trading accounts {'portfolio': X, 'cash': Y}
            personal_data: Personal accounts (optional)
            
        Returns:
            dict: Total net worth breakdown
        """
        # Business assets
        business_liquid = business_data.get('checking', 0) + business_data.get('tax_pot', 0)
        business_receivables = business_data.get('receivables', 0)
        total_business = business_liquid + business_receivables
        
        # Trading assets
        portfolio_value = trading_data.get('portfolio', 0)
        trading_cash = trading_data.get('cash', 0)
        total_trading = portfolio_value + trading_cash
        
        # Personal (if provided)
        total_personal = sum(personal_data.values()) if personal_data else 0
        
        # Total
        total_net_worth = total_business + total_trading + total_personal
        
        return {
            'total_net_worth': total_net_worth,
            'business_assets': {
                'total': total_business,
                'liquid': business_liquid,
                'receivables': business_receivables,
                'percentage': (total_business / total_net_worth * 100) if total_net_worth > 0 else 0
            },
            'trading_assets': {
                'total': total_trading,
                'portfolio': portfolio_value,
                'cash': trading_cash,
                'percentage': (total_trading / total_net_worth * 100) if total_net_worth > 0 else 0
            },
            'personal_assets': {
                'total': total_personal,
                'percentage': (total_personal / total_net_worth * 100) if total_net_worth > 0 else 0
            },
            'allocation': {
                'business': (total_business / total_net_worth * 100) if total_net_worth > 0 else 0,
                'trading': (total_trading / total_net_worth * 100) if total_net_worth > 0 else 0,
                'personal': (total_personal / total_net_worth * 100) if total_net_worth > 0 else 0
            }
        }
    
    @staticmethod
    def get_holistic_financial_health(business_metrics: Dict[str, Any],
                                      trading_metrics: Dict[str, Any],
                                      emotion_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall financial health combining all dimensions
        
        Args:
            business_metrics: Business health metrics
            trading_metrics: Trading performance metrics
            emotion_metrics: Emotional state metrics
            
        Returns:
            dict: Holistic health score and insights
        """
        # Business health (40% weight)
        business_score = business_metrics.get('financial_health_score', 0)
        business_weight = 0.40
        
        # Trading health (30% weight)
        trading_score = trading_metrics.get('portfolio_health_score', 0)
        trading_weight = 0.30
        
        # Emotional health (30% weight)
        # Higher calm, lower stress = better score
        calm_level = emotion_metrics.get('calm', 0)
        stress_level = emotion_metrics.get('stress', 0)
        emotion_score = (calm_level + (100 - stress_level)) / 2
        emotion_weight = 0.30
        
        # Weighted total
        total_score = (
            business_score * business_weight +
            trading_score * trading_weight +
            emotion_score * emotion_weight
        )
        
        # Grade
        if total_score >= 90:
            grade = 'A+'
            status = 'Excellent'
            color = 'green'
        elif total_score >= 80:
            grade = 'A'
            status = 'Very Good'
            color = 'green'
        elif total_score >= 70:
            grade = 'B'
            status = 'Good'
            color = 'yellow'
        elif total_score >= 60:
            grade = 'C'
            status = 'Fair'
            color = 'orange'
        else:
            grade = 'D'
            status = 'Needs Improvement'
            color = 'red'
        
        return {
            'total_score': total_score,
            'grade': grade,
            'status': status,
            'color': color,
            'components': {
                'business': {
                    'score': business_score,
                    'weight': business_weight,
                    'contribution': business_score * business_weight
                },
                'trading': {
                    'score': trading_score,
                    'weight': trading_weight,
                    'contribution': trading_score * trading_weight
                },
                'emotional': {
                    'score': emotion_score,
                    'weight': emotion_weight,
                    'contribution': emotion_score * emotion_weight
                }
            }
        }
    
    @staticmethod
    def get_emotion_impact_on_finances(emotion_history: pd.DataFrame,
                                      financial_decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze how emotions have impacted financial decisions
        
        Args:
            emotion_history: Historical emotion data
            financial_decisions: List of decisions made (trades, expenses, etc.)
            
        Returns:
            dict: Emotion impact analysis
        """
        if emotion_history.empty or not financial_decisions:
            return {
                'prevented_bad_decisions': 0,
                'optimal_decisions': 0,
                'total_saved': 0,
                'insights': []
            }
        
        prevented_count = 0
        optimal_count = 0
        total_saved = 0
        insights = []
        
        for decision in financial_decisions:
            decision_type = decision.get('type')  # 'trade', 'expense', 'invoice_delay'
            emotion_state = decision.get('emotion_state')
            outcome = decision.get('outcome')  # 'prevented', 'optimal', 'suboptimal'
            
            if outcome == 'prevented':
                prevented_count += 1
                saved = decision.get('estimated_loss_prevented', 0)
                total_saved += saved
                
                insights.append({
                    'type': 'prevention',
                    'message': f"Prevented {decision_type} when {emotion_state}",
                    'impact': f"Saved ${saved:.0f}"
                })
            
            elif outcome == 'optimal':
                optimal_count += 1
                
                insights.append({
                    'type': 'optimal',
                    'message': f"Made {decision_type} in optimal emotional state",
                    'impact': 'Positive'
                })
        
        return {
            'prevented_bad_decisions': prevented_count,
            'optimal_decisions': optimal_count,
            'total_saved': total_saved,
            'avg_prevention_value': total_saved / prevented_count if prevented_count > 0 else 0,
            'insights': insights[:10],  # Top 10
            'summary': f"Prevented {prevented_count} emotional decisions, saving ${total_saved:,.0f}"
        }
    
    @staticmethod
    def generate_smart_money_allocation(available_cash: float,
                                       business_needs: Dict[str, float],
                                       trading_opportunities: Dict[str, float],
                                       emotion_state: str) -> Dict[str, Any]:
        """
        Recommend optimal money allocation based on needs and opportunities
        
        Args:
            available_cash: Cash available to allocate
            business_needs: Business obligations {'taxes': X, 'bills': Y, 'buffer': Z}
            trading_opportunities: Trading opportunities {'quality_score': X, 'expected_return': Y}
            emotion_state: Current emotional state ('optimal', 'caution', 'warning')
            
        Returns:
            dict: Recommended allocation
        """
        allocation = {
            'tax_pot': 0,
            'business_buffer': 0,
            'emergency_fund': 0,
            'investment': 0,
            'discretionary': 0
        }
        
        remaining = available_cash
        
        # 1. Priority: Tax obligations (non-negotiable)
        tax_needed = business_needs.get('taxes', 0)
        allocation['tax_pot'] = min(tax_needed, remaining)
        remaining -= allocation['tax_pot']
        
        # 2. Priority: Essential business buffer
        buffer_needed = business_needs.get('buffer', 0)
        allocation['business_buffer'] = min(buffer_needed, remaining)
        remaining -= allocation['business_buffer']
        
        # 3. Priority: Emergency fund (3-6 months expenses)
        emergency_target = business_needs.get('emergency_fund_target', 0)
        emergency_current = business_needs.get('emergency_fund_current', 0)
        emergency_gap = max(0, emergency_target - emergency_current)
        allocation['emergency_fund'] = min(emergency_gap, remaining * 0.3)  # Max 30% of remaining
        remaining -= allocation['emergency_fund']
        
        # 4. Investment vs. Discretionary (depends on emotion state and opportunities)
        if emotion_state == 'optimal' and trading_opportunities.get('quality_score', 0) > 70:
            # Good state + good opportunities = invest more
            allocation['investment'] = remaining * 0.70
            allocation['discretionary'] = remaining * 0.30
        elif emotion_state == 'caution':
            # Moderate state = balanced
            allocation['investment'] = remaining * 0.50
            allocation['discretionary'] = remaining * 0.50
        else:
            # Warning state or poor opportunities = conservative
            allocation['investment'] = remaining * 0.20
            allocation['discretionary'] = remaining * 0.80
        
        # Generate recommendations
        recommendations = []
        
        if allocation['tax_pot'] < tax_needed:
            recommendations.append(f"⚠️ Tax pot underfunded by ${tax_needed - allocation['tax_pot']:,.0f}")
        
        if allocation['emergency_fund'] < emergency_gap:
            recommendations.append(f"💡 Continue building emergency fund (${emergency_gap - allocation['emergency_fund']:,.0f} more needed)")
        
        if emotion_state != 'optimal' and allocation['investment'] > 0:
            recommendations.append(f"⚠️ Consider delaying investments until emotional state improves")
        
        if not recommendations:
            recommendations.append("✅ Allocation looks good! All priorities covered.")
        
        return {
            'allocation': allocation,
            'total_allocated': sum(allocation.values()),
            'recommendations': recommendations,
            'emotion_adjusted': emotion_state != 'optimal',
            'breakdown_pct': {
                k: (v / available_cash * 100) if available_cash > 0 else 0 
                for k, v in allocation.items()
            }
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_income_streams_overview(business_income: pd.DataFrame,
                                   trading_income: pd.DataFrame,
                                   passive_income: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Analyze all income streams
        
        Args:
            business_income: Freelance/business income
            trading_income: Trading profits/losses
            passive_income: Dividends, interest, etc.
            
        Returns:
            dict: Income streams analysis
        """
        streams = {}
        total_income = 0
        
        # Business income
        if not business_income.empty:
            business_total = business_income['amount'].sum()
            streams['business'] = {
                'total': business_total,
                'avg_monthly': business_total / max(1, business_income['date'].dt.to_period('M').nunique()),
                'consistency_score': UnifiedInsights._calculate_consistency(business_income),
                'trend': 'up' if business_income['amount'].iloc[-5:].mean() > business_income['amount'].iloc[:5].mean() else 'down'
            }
            total_income += business_total
        
        # Trading income
        if not trading_income.empty:
            trading_total = trading_income['amount'].sum()
            streams['trading'] = {
                'total': trading_total,
                'avg_monthly': trading_total / max(1, trading_income['date'].dt.to_period('M').nunique()),
                'consistency_score': UnifiedInsights._calculate_consistency(trading_income),
                'volatility': trading_income['amount'].std()
            }
            total_income += trading_total
        
        # Passive income
        if passive_income is not None and not passive_income.empty:
            passive_total = passive_income['amount'].sum()
            streams['passive'] = {
                'total': passive_total,
                'avg_monthly': passive_total / max(1, passive_income['date'].dt.to_period('M').nunique()),
                'consistency_score': UnifiedInsights._calculate_consistency(passive_income)
            }
            total_income += passive_total
        
        # Calculate percentages
        for stream in streams.values():
            stream['percentage'] = (stream['total'] / total_income * 100) if total_income > 0 else 0
        
        return {
            'total_income': total_income,
            'streams': streams,
            'num_streams': len(streams),
            'diversification_score': min(100, len(streams) * 25),  # 25 points per stream, max 100
            'primary_stream': max(streams.items(), key=lambda x: x[1]['total'])[0] if streams else None
        }
    
    @staticmethod
    def _calculate_consistency(income_df: pd.DataFrame) -> float:
        """Calculate income consistency score (0-100)"""
        if income_df.empty or len(income_df) < 2:
            return 0
        
        # Group by month
        monthly = income_df.groupby(income_df['date'].dt.to_period('M'))['amount'].sum()
        
        if len(monthly) < 2:
            return 50
        
        # Calculate coefficient of variation (lower is more consistent)
        mean = monthly.mean()
        std = monthly.std()
        
        if mean == 0:
            return 0
        
        cv = std / mean
        
        # Convert to 0-100 score (lower CV = higher score)
        # CV of 0 = 100, CV of 1 = 0
        score = max(0, min(100, 100 - (cv * 100)))
        
        return score
    
    @staticmethod
    def get_daily_financial_brief(date: datetime,
                                  business_data: Dict[str, Any],
                                  trading_data: Dict[str, Any],
                                  emotion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate daily financial briefing
        
        Args:
            date: Date for briefing
            business_data: Business stats for the day
            trading_data: Trading stats for the day
            emotion_data: Emotion data for the day
            
        Returns:
            dict: Daily brief
        """
        brief = {
            'date': date,
            'highlights': [],
            'alerts': [],
            'recommendations': [],
            'emoji_status': ''
        }
        
        # Business highlights
        invoices_paid = business_data.get('invoices_paid', 0)
        revenue_today = business_data.get('revenue', 0)
        
        if invoices_paid > 0:
            brief['highlights'].append(f"💰 {invoices_paid} invoice(s) paid today (${revenue_today:,.0f})")
        
        # Trading highlights
        portfolio_change = trading_data.get('portfolio_change_pct', 0)
        if abs(portfolio_change) > 2:
            emoji = '📈' if portfolio_change > 0 else '📉'
            brief['highlights'].append(f"{emoji} Portfolio {portfolio_change:+.1f}% today")
        
        # Emotion alerts
        emotion_state = emotion_data.get('state', 'neutral')
        if emotion_state == 'stressed':
            brief['alerts'].append("⚠️ High stress detected - avoid major financial decisions")
        elif emotion_state == 'optimal':
            brief['highlights'].append("✅ Optimal emotional state for decision-making")
        
        # Upcoming obligations
        bills_due_soon = business_data.get('bills_due_soon', [])
        if bills_due_soon:
            brief['alerts'].append(f"💳 {len(bills_due_soon)} bill(s) due this week")
        
        # Recommendations
        if emotion_state == 'optimal' and revenue_today > 0:
            brief['recommendations'].append("💡 Good time to allocate today's revenue to tax/investment")
        
        # Overall status emoji
        if brief['alerts']:
            brief['emoji_status'] = '⚠️'
        elif brief['highlights']:
            brief['emoji_status'] = '✅'
        else:
            brief['emoji_status'] = '📊'
        
        return brief

