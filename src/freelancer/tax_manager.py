"""
Tax Manager Module
Handles tax estimates, savings automation, quarterly reminders, and 1099 management
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import streamlit as st
import pandas as pd

class TaxManager:
    """Manages tax calculations and compliance for freelancers"""
    
    # 2024 Tax brackets (simplified - federal only for demo)
    TAX_BRACKETS_SINGLE = [
        (11600, 0.10),   # 10% up to $11,600
        (47150, 0.12),   # 12% up to $47,150
        (100525, 0.22),  # 22% up to $100,525
        (191950, 0.24),  # 24% up to $191,950
        (243725, 0.32),  # 32% up to $243,725
        (609350, 0.35),  # 35% up to $609,350
        (float('inf'), 0.37)  # 37% above
    ]
    
    # Standard deduction 2024
    STANDARD_DEDUCTION = 14600
    
    # Self-employment tax rate
    SE_TAX_RATE = 0.153  # 15.3% (Social Security + Medicare)
    SE_DEDUCTION = 0.9235  # Only pay SE tax on 92.35% of net earnings
    
    @staticmethod
    def estimate_taxes(gross_income: float, deductible_expenses: float,
                      state_tax_rate: float = 0.05,
                      filing_status: str = 'single') -> Dict[str, Any]:
        """
        Calculate comprehensive tax estimates
        
        Args:
            gross_income: Total income for the year
            deductible_expenses: Business expenses
            state_tax_rate: State income tax rate (default 5%)
            filing_status: 'single', 'married_joint', 'married_separate', 'head_of_household'
            
        Returns:
            dict: Tax estimates broken down by type
        """
        # Calculate net income
        net_income = gross_income - deductible_expenses
        
        # Calculate self-employment tax
        se_taxable = net_income * TaxManager.SE_DEDUCTION
        se_tax = se_taxable * TaxManager.SE_TAX_RATE
        
        # Half of SE tax is deductible
        se_tax_deduction = se_tax / 2
        
        # Calculate AGI
        agi = net_income - se_tax_deduction
        
        # Apply standard deduction
        taxable_income = max(0, agi - TaxManager.STANDARD_DEDUCTION)
        
        # Calculate federal income tax (progressive)
        federal_tax = TaxManager._calculate_progressive_tax(
            taxable_income, 
            TaxManager.TAX_BRACKETS_SINGLE
        )
        
        # Calculate state tax (simplified flat rate)
        state_tax = taxable_income * state_tax_rate
        
        # Total tax
        total_tax = federal_tax + state_tax + se_tax
        
        # Effective tax rate
        effective_rate = (total_tax / gross_income * 100) if gross_income > 0 else 0
        
        # Quarterly estimate
        quarterly = total_tax / 4
        
        # Next quarterly due dates
        quarterly_dates = TaxManager._get_quarterly_due_dates()
        
        return {
            'gross_income': gross_income,
            'deductible_expenses': deductible_expenses,
            'net_income': net_income,
            'agi': agi,
            'taxable_income': taxable_income,
            'federal_tax': federal_tax,
            'state_tax': state_tax,
            'self_employment_tax': se_tax,
            'total_estimated_tax': total_tax,
            'effective_tax_rate': effective_rate,
            'quarterly_payment': quarterly,
            'quarterly_due_dates': quarterly_dates,
            'next_due_date': TaxManager._get_next_due_date(quarterly_dates),
            'recommended_savings_pct': min(35, max(25, effective_rate + 5)),  # Add 5% buffer
            'breakdown': {
                'federal_pct': (federal_tax / total_tax * 100) if total_tax > 0 else 0,
                'state_pct': (state_tax / total_tax * 100) if total_tax > 0 else 0,
                'se_pct': (se_tax / total_tax * 100) if total_tax > 0 else 0
            }
        }
    
    @staticmethod
    def _calculate_progressive_tax(income: float, brackets: List[tuple]) -> float:
        """Calculate tax using progressive brackets"""
        tax = 0
        previous_limit = 0
        
        for limit, rate in brackets:
            if income <= previous_limit:
                break
            
            taxable_in_bracket = min(income, limit) - previous_limit
            tax += taxable_in_bracket * rate
            previous_limit = limit
        
        return tax
    
    @staticmethod
    def _get_quarterly_due_dates() -> List[Dict[str, Any]]:
        """Get quarterly estimated tax due dates"""
        today = datetime.now()
        year = today.year
        
        # Quarterly due dates for estimated taxes
        dates = [
            {'quarter': 'Q1', 'date': datetime(year, 4, 15), 'period': f'Jan 1 - Mar 31, {year}'},
            {'quarter': 'Q2', 'date': datetime(year, 6, 15), 'period': f'Apr 1 - May 31, {year}'},
            {'quarter': 'Q3', 'date': datetime(year, 9, 15), 'period': f'Jun 1 - Aug 31, {year}'},
            {'quarter': 'Q4', 'date': datetime(year + 1, 1, 15), 'period': f'Sep 1 - Dec 31, {year}'}
        ]
        
        return dates
    
    @staticmethod
    def _get_next_due_date(quarterly_dates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get next upcoming quarterly due date"""
        today = datetime.now()
        
        for q in quarterly_dates:
            if q['date'] > today:
                return q
        
        # If all dates passed, return first quarter of next year
        return quarterly_dates[0] if quarterly_dates else None
    
    @staticmethod
    def auto_transfer_to_tax_pot(income_amount: float, 
                                 savings_percentage: float,
                                 from_account: str,
                                 to_account: str) -> Dict[str, Any]:
        """
        Automatically transfer a percentage of income to tax savings
        
        Args:
            income_amount: Amount of income received
            savings_percentage: Percentage to save for taxes
            from_account: Source account
            to_account: Tax savings account
            
        Returns:
            dict: Transfer details
        """
        transfer_amount = income_amount * (savings_percentage / 100)
        
        return {
            'transfer_id': "tax_transfer_" + ''.join(random.choices('0123456789', k=12)),
            'from_account': from_account,
            'to_account': to_account,
            'income_amount': income_amount,
            'savings_percentage': savings_percentage,
            'transfer_amount': transfer_amount,
            'transferred_at': datetime.now(),
            'status': 'completed',
            'rule': f"Auto-save {savings_percentage}% for taxes"
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def categorize_expenses_for_taxes(expenses_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Categorize expenses for tax deduction purposes
        
        Args:
            expenses_df: DataFrame of expenses with 'category', 'amount', 'tax_deductible'
            
        Returns:
            dict: Tax categorization summary
        """
        if expenses_df.empty:
            return {
                'total_expenses': 0,
                'deductible_expenses': 0,
                'non_deductible_expenses': 0,
                'by_category': {}
            }
        
        total = expenses_df['amount'].sum()
        deductible = expenses_df[expenses_df['tax_deductible'] == True]['amount'].sum()
        non_deductible = total - deductible
        
        # Group by category
        by_category = {}
        for category in expenses_df['category'].unique():
            category_data = expenses_df[expenses_df['category'] == category]
            by_category[category] = {
                'total': category_data['amount'].sum(),
                'deductible': category_data[category_data['tax_deductible'] == True]['amount'].sum(),
                'count': len(category_data)
            }
        
        return {
            'total_expenses': total,
            'deductible_expenses': deductible,
            'non_deductible_expenses': non_deductible,
            'deduction_rate': (deductible / total * 100) if total > 0 else 0,
            'by_category': by_category
        }
    
    @staticmethod
    def generate_1099_data(contractors: List[Dict[str, Any]],
                          year: int = None) -> List[Dict[str, Any]]:
        """
        Generate 1099-NEC data for contractors paid > $600
        
        Args:
            contractors: List of contractor payment records
            year: Tax year (defaults to current)
            
        Returns:
            list: 1099-NEC forms to file
        """
        if year is None:
            year = datetime.now().year
        
        forms = []
        
        for contractor in contractors:
            total_paid = contractor.get('total_paid', 0)
            
            # Only need to file if paid $600 or more
            if total_paid >= 600:
                forms.append({
                    'form_type': '1099-NEC',
                    'tax_year': year,
                    'recipient_name': contractor.get('name'),
                    'recipient_tin': contractor.get('tin', 'NOT PROVIDED'),
                    'recipient_address': contractor.get('address', {}),
                    'amount_paid': total_paid,
                    'nonemployee_compensation': total_paid,  # Box 1
                    'federal_tax_withheld': contractor.get('withheld', 0),  # Box 4
                    'filing_required': True,
                    'filing_deadline': datetime(year + 1, 1, 31),
                    'w9_on_file': contractor.get('w9_received', False)
                })
        
        return forms
    
    @staticmethod
    def collect_w9(contractor_email: str) -> Dict[str, Any]:
        """
        Initiate W-9 collection from contractor
        
        Args:
            contractor_email: Contractor email address
            
        Returns:
            dict: W-9 request details
        """
        request_id = "w9_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        
        return {
            'request_id': request_id,
            'contractor_email': contractor_email,
            'form_type': 'W-9',
            'status': 'sent',
            'sent_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(days=30),
            'completion_link': f"https://forms.pulsetrade.com/w9/{request_id}",
            'reminder_schedule': [7, 14, 21]  # Days until reminders
        }
    
    @staticmethod
    def export_for_cpa(income_data: Dict[str, Any],
                      expense_data: pd.DataFrame,
                      format: str = 'csv') -> Dict[str, Any]:
        """
        Export tax data for CPA
        
        Args:
            income_data: Income summary
            expense_data: Expense DataFrame
            format: Export format ('csv', 'excel', 'pdf')
            
        Returns:
            dict: Export details
        """
        export_id = "export_" + ''.join(random.choices('0123456789ABCDEF', k=12))
        
        return {
            'export_id': export_id,
            'format': format,
            'year': datetime.now().year,
            'includes': [
                'Income summary',
                'Expense breakdown',
                'Tax estimates',
                'Quarterly payments made',
                '1099 forms received',
                'Business deductions'
            ],
            'file_url': f"https://exports.pulsetrade.com/{export_id}.{format}",
            'generated_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(days=30)
        }
    
    @staticmethod
    def get_tax_savings_status(account_balance: float,
                              ytd_income: float,
                              ytd_taxes_saved: float,
                              recommended_rate: float) -> Dict[str, Any]:
        """
        Check if user is on track with tax savings
        
        Args:
            account_balance: Current tax savings account balance
            ytd_income: Year-to-date income
            ytd_taxes_saved: Year-to-date amount saved for taxes
            recommended_rate: Recommended savings rate (%)
            
        Returns:
            dict: Tax savings status
        """
        recommended_savings = ytd_income * (recommended_rate / 100)
        difference = ytd_taxes_saved - recommended_savings
        
        if difference >= 0:
            status = 'on_track'
            message = f"✅ You're on track! Saved {ytd_taxes_saved:,.0f} (recommended: ${recommended_savings:,.0f})"
        elif difference > -500:
            status = 'slightly_behind'
            message = f"⚠️ Slightly behind. Saved ${ytd_taxes_saved:,.0f}, recommend ${recommended_savings:,.0f}"
        else:
            status = 'behind'
            message = f"🚨 Behind on tax savings! Saved ${ytd_taxes_saved:,.0f}, should be ${recommended_savings:,.0f}"
        
        return {
            'status': status,
            'message': message,
            'account_balance': account_balance,
            'ytd_income': ytd_income,
            'ytd_taxes_saved': ytd_taxes_saved,
            'recommended_savings': recommended_savings,
            'difference': difference,
            'on_track_percentage': (ytd_taxes_saved / recommended_savings * 100) if recommended_savings > 0 else 0,
            'catch_up_needed': max(0, -difference)
        }
    
    @staticmethod
    def get_deduction_tips(expenses_df: pd.DataFrame) -> List[str]:
        """
        Get personalized tax deduction tips
        
        Args:
            expenses_df: Expense DataFrame
            
        Returns:
            list: Tax saving tips
        """
        tips = []
        
        if expenses_df.empty:
            return [
                "💡 Track all business expenses to maximize deductions",
                "💡 Home office deduction can save $1,000+ per year",
                "💡 Keep receipts for all purchases over $75"
            ]
        
        # Check for common deduction opportunities
        categories = expenses_df['category'].unique()
        
        if 'Office Supplies' not in categories:
            tips.append("💡 Don't forget to track office supplies - 100% deductible")
        
        if 'Internet & Phone' not in categories:
            tips.append("💡 Business use of internet/phone is deductible (pro-rated for business %)")
        
        if 'Professional Services' not in categories:
            tips.append("💡 Accounting and legal fees are fully deductible")
        
        if 'Education' not in categories:
            tips.append("💡 Courses and books related to your business are deductible")
        
        # Check for home office
        home_office_expenses = expenses_df[expenses_df['description'].str.contains('home|office|rent', case=False, na=False)]
        if home_office_expenses.empty:
            tips.append("💡 Home office deduction: Deduct portion of rent/mortgage, utilities")
        
        # Check for vehicle expenses
        vehicle_expenses = expenses_df[expenses_df['category'].str.contains('travel|gas|vehicle', case=False, na=False)]
        if vehicle_expenses.empty:
            tips.append("💡 Track business mileage - Standard mileage rate is 67¢/mile (2024)")
        
        # Check for health insurance
        health_expenses = expenses_df[expenses_df['description'].str.contains('health|insurance', case=False, na=False)]
        if health_expenses.empty:
            tips.append("💡 Self-employed health insurance premiums are 100% deductible")
        
        # Check for retirement contributions
        retirement_expenses = expenses_df[expenses_df['description'].str.contains('401k|ira|sep', case=False, na=False)]
        if retirement_expenses.empty:
            tips.append("💡 SEP-IRA or Solo 401(k) contributions reduce your taxable income")
        
        # Default tips if nothing specific found
        if not tips:
            tips = [
                "✅ Great expense tracking! Keep it up",
                "💡 Review quarterly to catch any missed deductions",
                "💡 Consider a SEP-IRA to save for retirement + reduce taxes"
            ]
        
        return tips[:5]  # Return top 5 tips

