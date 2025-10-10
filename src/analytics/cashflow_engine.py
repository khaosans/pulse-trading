"""
Cash Flow Engine Module
Provides cash flow forecasting, runway calculation, and financial insights
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st

class CashFlowEngine:
    """Manages cash flow analysis and forecasting for freelancers"""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def forecast_cash_flow(income_history: pd.DataFrame,
                          expense_history: pd.DataFrame,
                          outstanding_invoices: List[Dict[str, Any]],
                          forecast_days: int = 90) -> Dict[str, Any]:
        """
        Forecast cash flow for next N days
        
        Args:
            income_history: Historical income data
            expense_history: Historical expense data
            outstanding_invoices: Invoices awaiting payment
            forecast_days: Days to forecast
            
        Returns:
            dict: Cash flow forecast with confidence bands
        """
        # Calculate historical patterns
        if not income_history.empty:
            avg_monthly_income = income_history.groupby(
                income_history['date'].dt.to_period('M')
            )['amount'].sum().mean()
        else:
            avg_monthly_income = 5000  # Default
        
        if not expense_history.empty:
            avg_monthly_expenses = expense_history.groupby(
                expense_history['date'].dt.to_period('M')
            )['amount'].sum().mean()
        else:
            avg_monthly_expenses = 2000  # Default
        
        # Detect seasonality (simplified)
        seasonality_factor = CashFlowEngine._detect_seasonality(income_history)
        
        # Project future dates
        forecast_dates = pd.date_range(
            start=datetime.now(),
            periods=forecast_days,
            freq='D'
        )
        
        # Project income
        daily_income_base = avg_monthly_income / 30
        projected_income = []
        
        for i, date in enumerate(forecast_dates):
            # Apply seasonality
            seasonal_mult = seasonality_factor.get(date.month, 1.0)
            
            # Add some randomness but trending toward average
            income = daily_income_base * seasonal_mult * np.random.uniform(0.7, 1.3)
            
            # Add known invoices
            for inv in outstanding_invoices:
                inv_due = inv.get('due_date')
                if isinstance(inv_due, str):
                    inv_due = datetime.fromisoformat(inv_due)
                
                if inv_due and inv_due.date() == date.date():
                    # 70% probability they pay on time
                    if np.random.random() < 0.7:
                        income += inv.get('total', 0)
            
            projected_income.append(income)
        
        # Project expenses
        daily_expense_base = avg_monthly_expenses / 30
        projected_expenses = []
        
        for i, date in enumerate(forecast_dates):
            # Expenses more stable than income
            expense = daily_expense_base * np.random.uniform(0.8, 1.2)
            projected_expenses.append(expense)
        
        # Calculate cumulative cash flow
        net_daily = np.array(projected_income) - np.array(projected_expenses)
        cumulative_cf = np.cumsum(net_daily)
        
        # Calculate confidence bands (simulate uncertainty)
        confidence_high = cumulative_cf * 1.2
        confidence_low = cumulative_cf * 0.8
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'projected_income': projected_income,
            'projected_expenses': projected_expenses,
            'net_cash_flow': net_daily,
            'cumulative_cash_flow': cumulative_cf,
            'confidence_high': confidence_high,
            'confidence_low': confidence_low
        })
        
        return {
            'forecast': forecast_df,
            'summary': {
                'avg_monthly_income': avg_monthly_income,
                'avg_monthly_expenses': avg_monthly_expenses,
                'avg_monthly_net': avg_monthly_income - avg_monthly_expenses,
                'forecast_end_balance': cumulative_cf[-1],
                'total_projected_income': sum(projected_income),
                'total_projected_expenses': sum(projected_expenses),
                'forecast_accuracy': 'Medium'  # Based on historical data volume
            }
        }
    
    @staticmethod
    def _detect_seasonality(income_history: pd.DataFrame) -> Dict[int, float]:
        """Detect seasonal patterns in income"""
        if income_history.empty or len(income_history) < 180:  # Need 6+ months
            return {i: 1.0 for i in range(1, 13)}  # No seasonality
        
        # Group by month and calculate average
        monthly_avg = income_history.groupby(
            income_history['date'].dt.month
        )['amount'].mean()
        
        overall_avg = monthly_avg.mean()
        
        # Calculate seasonal factors
        seasonal_factors = {}
        for month in range(1, 13):
            if month in monthly_avg.index:
                seasonal_factors[month] = monthly_avg[month] / overall_avg
            else:
                seasonal_factors[month] = 1.0
        
        return seasonal_factors
    
    @staticmethod
    def calculate_runway(current_balance: float,
                        monthly_burn_rate: float,
                        monthly_income: float = 0) -> Dict[str, Any]:
        """
        Calculate financial runway
        
        Args:
            current_balance: Current cash balance
            monthly_burn_rate: Monthly expenses
            monthly_income: Expected monthly income
            
        Returns:
            dict: Runway calculation
        """
        net_burn = monthly_burn_rate - monthly_income
        
        if net_burn <= 0:
            return {
                'runway_months': float('inf'),
                'runway_days': float('inf'),
                'cash_positive': True,
                'message': '✅ You are cash flow positive! No runway concerns.',
                'recommendation': 'Consider investing surplus cash or building emergency fund.'
            }
        
        runway_months = current_balance / net_burn
        runway_days = runway_months * 30
        
        if runway_months < 3:
            status = 'critical'
            message = f'🚨 Critical: Only {runway_months:.1f} months runway'
            recommendation = 'Reduce expenses immediately and focus on revenue generation'
        elif runway_months < 6:
            status = 'warning'
            message = f'⚠️ Warning: {runway_months:.1f} months runway'
            recommendation = 'Build cash reserves and consider reducing expenses'
        elif runway_months < 12:
            status = 'fair'
            message = f'💡 Fair: {runway_months:.1f} months runway'
            recommendation = 'Continue building reserves to reach 12+ months'
        else:
            status = 'healthy'
            message = f'✅ Healthy: {runway_months:.1f} months runway'
            recommendation = 'Maintain current trajectory and invest wisely'
        
        return {
            'runway_months': runway_months,
            'runway_days': runway_days,
            'current_balance': current_balance,
            'monthly_burn_rate': monthly_burn_rate,
            'monthly_income': monthly_income,
            'net_monthly_burn': net_burn,
            'cash_positive': False,
            'status': status,
            'message': message,
            'recommendation': recommendation,
            'zero_cash_date': datetime.now() + timedelta(days=runway_days)
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def analyze_income_diversity(clients: List[Dict[str, Any]],
                                 income_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze income concentration risk
        
        Args:
            clients: List of client data
            income_data: Income transaction history
            
        Returns:
            dict: Income diversity analysis
        """
        if not clients:
            return {
                'concentration_score': 0,
                'top_client_percentage': 0,
                'herfindahl_index': 0,
                'risk_level': 'unknown'
            }
        
        # Calculate revenue by client
        client_revenue = {}
        total_revenue = 0
        
        for client in clients:
            client_id = client.get('client_id')
            revenue = client.get('total_paid', 0)
            client_revenue[client_id] = revenue
            total_revenue += revenue
        
        if total_revenue == 0:
            return {
                'concentration_score': 0,
                'top_client_percentage': 0,
                'herfindahl_index': 0,
                'risk_level': 'unknown'
            }
        
        # Calculate concentration metrics
        # Sort by revenue
        sorted_clients = sorted(client_revenue.items(), key=lambda x: x[1], reverse=True)
        
        # Top client percentage
        top_client_pct = (sorted_clients[0][1] / total_revenue * 100) if sorted_clients else 0
        
        # Top 3 clients percentage
        top_3_pct = sum(c[1] for c in sorted_clients[:3]) / total_revenue * 100 if len(sorted_clients) >= 3 else top_client_pct
        
        # Herfindahl-Hirschman Index (HHI) - concentration measure
        # HHI = sum of squared market shares (0-10,000)
        # <1,500 = low concentration, 1,500-2,500 = moderate, >2,500 = high
        hhi = sum((rev / total_revenue * 100) ** 2 for rev in client_revenue.values())
        
        # Determine risk level
        if top_client_pct > 50 or hhi > 2500:
            risk_level = 'high'
            risk_message = f'🚨 High concentration risk: Top client is {top_client_pct:.0f}% of revenue'
            recommendation = 'Diversify client base urgently - loss of top client would be severe'
        elif top_client_pct > 30 or hhi > 1500:
            risk_level = 'moderate'
            risk_message = f'⚠️ Moderate concentration: Top client is {top_client_pct:.0f}% of revenue'
            recommendation = 'Work on acquiring 2-3 more similar-sized clients to reduce risk'
        else:
            risk_level = 'low'
            risk_message = f'✅ Well diversified: Top client is {top_client_pct:.0f}% of revenue'
            recommendation = 'Maintain current client diversity while growing total revenue'
        
        return {
            'total_revenue': total_revenue,
            'num_clients': len(clients),
            'top_client_percentage': top_client_pct,
            'top_3_percentage': top_3_pct,
            'herfindahl_index': hhi,
            'risk_level': risk_level,
            'risk_message': risk_message,
            'recommendation': recommendation,
            'concentration_score': min(100, hhi / 25),  # Normalize to 0-100
            'top_clients': [
                {
                    'client_id': c[0],
                    'revenue': c[1],
                    'percentage': c[1] / total_revenue * 100
                }
                for c in sorted_clients[:5]
            ]
        }
    
    @staticmethod
    def scenario_analysis(current_balance: float,
                         monthly_income: float,
                         monthly_expenses: float,
                         scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run what-if scenario analysis
        
        Args:
            current_balance: Current cash balance
            monthly_income: Current monthly income
            monthly_expenses: Current monthly expenses
            scenarios: List of scenario definitions
            
        Returns:
            list: Scenario analysis results
        """
        results = []
        
        # Base case
        base_net = monthly_income - monthly_expenses
        base_runway = current_balance / (monthly_expenses - monthly_income) if monthly_expenses > monthly_income else float('inf')
        
        results.append({
            'name': 'Current Baseline',
            'type': 'baseline',
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'net_monthly': base_net,
            'runway_months': base_runway,
            'balance_in_6_months': current_balance + (base_net * 6),
            'balance_in_12_months': current_balance + (base_net * 12)
        })
        
        # Run each scenario
        for scenario in scenarios:
            income_change = scenario.get('income_change_pct', 0)
            expense_change = scenario.get('expense_change_pct', 0)
            
            new_income = monthly_income * (1 + income_change / 100)
            new_expenses = monthly_expenses * (1 + expense_change / 100)
            new_net = new_income - new_expenses
            new_runway = current_balance / (new_expenses - new_income) if new_expenses > new_income else float('inf')
            
            results.append({
                'name': scenario.get('name', 'Scenario'),
                'type': 'scenario',
                'description': scenario.get('description', ''),
                'monthly_income': new_income,
                'monthly_expenses': new_expenses,
                'net_monthly': new_net,
                'runway_months': new_runway,
                'balance_in_6_months': current_balance + (new_net * 6),
                'balance_in_12_months': current_balance + (new_net * 12),
                'vs_baseline': {
                    'income_delta': new_income - monthly_income,
                    'expense_delta': new_expenses - monthly_expenses,
                    'net_delta': new_net - base_net,
                    'runway_delta': new_runway - base_runway if base_runway != float('inf') else 0
                }
            })
        
        return results
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_financial_health_score(balance: float,
                                   monthly_income: float,
                                   monthly_expenses: float,
                                   debt: float,
                                   emergency_fund: float,
                                   income_diversity_score: float) -> Dict[str, Any]:
        """
        Calculate overall financial health score (0-100)
        
        Args:
            balance: Current balance
            monthly_income: Monthly income
            monthly_expenses: Monthly expenses
            debt: Total debt
            emergency_fund: Emergency fund balance
            income_diversity_score: Income concentration score (0-100, lower is better)
            
        Returns:
            dict: Financial health assessment
        """
        score_components = {}
        
        # 1. Runway (30 points max)
        runway_months = balance / monthly_expenses if monthly_expenses > 0 else 12
        if runway_months >= 12:
            runway_score = 30
        elif runway_months >= 6:
            runway_score = 20
        elif runway_months >= 3:
            runway_score = 10
        else:
            runway_score = 5
        score_components['runway'] = runway_score
        
        # 2. Cash flow (25 points max)
        net_cash_flow = monthly_income - monthly_expenses
        if net_cash_flow > monthly_expenses * 0.3:  # 30% profit margin
            cashflow_score = 25
        elif net_cash_flow > 0:
            cashflow_score = 15
        elif net_cash_flow > -monthly_expenses * 0.2:
            cashflow_score = 5
        else:
            cashflow_score = 0
        score_components['cash_flow'] = cashflow_score
        
        # 3. Debt burden (20 points max)
        if debt == 0:
            debt_score = 20
        elif debt < monthly_income * 3:
            debt_score = 15
        elif debt < monthly_income * 6:
            debt_score = 10
        else:
            debt_score = 5
        score_components['debt'] = debt_score
        
        # 4. Emergency fund (15 points max)
        emergency_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
        if emergency_months >= 6:
            emergency_score = 15
        elif emergency_months >= 3:
            emergency_score = 10
        else:
            emergency_score = emergency_months * 2
        score_components['emergency_fund'] = emergency_score
        
        # 5. Income diversity (10 points max)
        # Lower diversity score is better, so invert it
        diversity_score = max(0, 10 - (income_diversity_score / 10))
        score_components['income_diversity'] = diversity_score
        
        # Total score
        total_score = sum(score_components.values())
        
        # Grade
        if total_score >= 90:
            grade = 'A+'
            status = 'Excellent'
        elif total_score >= 80:
            grade = 'A'
            status = 'Very Good'
        elif total_score >= 70:
            grade = 'B'
            status = 'Good'
        elif total_score >= 60:
            grade = 'C'
            status = 'Fair'
        else:
            grade = 'D'
            status = 'Needs Improvement'
        
        return {
            'total_score': total_score,
            'grade': grade,
            'status': status,
            'components': score_components,
            'max_possible': 100,
            'recommendations': CashFlowEngine._get_health_recommendations(score_components)
        }
    
    @staticmethod
    def _get_health_recommendations(components: Dict[str, float]) -> List[str]:
        """Generate recommendations based on score components"""
        recommendations = []
        
        if components.get('runway', 0) < 20:
            recommendations.append('🎯 Priority: Build cash reserves to 6+ months of expenses')
        
        if components.get('cash_flow', 0) < 15:
            recommendations.append('💰 Focus on increasing revenue or reducing expenses')
        
        if components.get('debt', 0) < 15:
            recommendations.append('💳 Pay down debt to improve financial flexibility')
        
        if components.get('emergency_fund', 0) < 10:
            recommendations.append('🏦 Build emergency fund to 3-6 months expenses')
        
        if components.get('income_diversity', 0) < 7:
            recommendations.append('🎲 Diversify client base to reduce concentration risk')
        
        if not recommendations:
            recommendations.append('✅ Great financial health! Focus on growth and investment')
        
        return recommendations

