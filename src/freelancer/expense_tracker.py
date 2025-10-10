"""
Expense Tracker Module
Handles expense categorization, receipt capture, and accounting sync
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import streamlit as st
import pandas as pd
from dataclasses import dataclass, asdict

@dataclass
class Expense:
    """Business expense"""
    expense_id: str
    date: datetime
    merchant: str
    description: str
    amount: float
    category: str
    subcategory: Optional[str]
    payment_method: str
    tax_deductible: bool
    deduction_percentage: float  # For partial deductions (e.g., 50% meals)
    receipt_url: Optional[str]
    notes: str
    synced_to_accounting: bool

class ExpenseTracker:
    """Manages expense tracking and categorization"""
    
    # IRS expense categories for freelancers/small business
    EXPENSE_CATEGORIES = {
        'Advertising & Marketing': {
            'subcategories': ['Online Ads', 'Print Ads', 'Social Media', 'SEO', 'Content Marketing'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Software & Tools': {
            'subcategories': ['Subscriptions', 'Licenses', 'Cloud Services', 'Design Tools', 'Dev Tools'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Office Supplies': {
            'subcategories': ['Stationery', 'Equipment', 'Furniture', 'Postage'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Professional Services': {
            'subcategories': ['Legal', 'Accounting', 'Consulting', 'Coaching'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Internet & Phone': {
            'subcategories': ['Internet', 'Mobile Phone', 'Landline'],
            'deductible': True,
            'deduction_pct': 100  # Business portion only
        },
        'Travel': {
            'subcategories': ['Flights', 'Hotels', 'Car Rental', 'Mileage', 'Parking'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Meals & Entertainment': {
            'subcategories': ['Client Meals', 'Business Meals', 'Team Meals'],
            'deductible': True,
            'deduction_pct': 50  # Only 50% deductible
        },
        'Education & Training': {
            'subcategories': ['Courses', 'Books', 'Conferences', 'Certifications'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Insurance': {
            'subcategories': ['Liability', 'Professional', 'Health', 'Business'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Home Office': {
            'subcategories': ['Rent', 'Utilities', 'Maintenance', 'Depreciation'],
            'deductible': True,
            'deduction_pct': 100  # Prorated for business use
        },
        'Bank & Finance': {
            'subcategories': ['Bank Fees', 'Merchant Fees', 'Interest', 'Credit Card Fees'],
            'deductible': True,
            'deduction_pct': 100
        },
        'Other': {
            'subcategories': ['Miscellaneous'],
            'deductible': False,
            'deduction_pct': 0
        }
    }
    
    @staticmethod
    def auto_categorize_expense(merchant: str, description: str, 
                               amount: float) -> Dict[str, Any]:
        """
        Auto-categorize expense using ML simulation
        
        Args:
            merchant: Merchant name
            description: Transaction description
            amount: Transaction amount
            
        Returns:
            dict: Categorization with confidence score
        """
        # Simulate ML categorization with keyword matching
        merchant_lower = merchant.lower()
        desc_lower = description.lower()
        
        # Pattern matching rules (simulating ML)
        if any(word in merchant_lower for word in ['adobe', 'github', 'figma', 'notion', 'slack']):
            category = 'Software & Tools'
            confidence = 0.95
        elif any(word in merchant_lower for word in ['amazon', 'staples', 'office']):
            category = 'Office Supplies'
            confidence = 0.90
        elif any(word in merchant_lower for word in ['google', 'facebook', 'linkedin', 'ads']):
            category = 'Advertising & Marketing'
            confidence = 0.92
        elif any(word in merchant_lower for word in ['legal', 'attorney', 'lawyer', 'accountant']):
            category = 'Professional Services'
            confidence = 0.88
        elif any(word in merchant_lower for word in ['verizon', 'at&t', 'comcast', 'internet', 'phone']):
            category = 'Internet & Phone'
            confidence = 0.85
        elif any(word in merchant_lower for word in ['airline', 'hotel', 'uber', 'lyft', 'rental car']):
            category = 'Travel'
            confidence = 0.87
        elif any(word in merchant_lower for word in ['restaurant', 'cafe', 'starbucks', 'lunch', 'dinner']):
            category = 'Meals & Entertainment'
            confidence = 0.80
        elif any(word in merchant_lower for word in ['udemy', 'coursera', 'book', 'conference']):
            category = 'Education & Training'
            confidence = 0.90
        else:
            category = 'Other'
            confidence = 0.50
        
        cat_info = ExpenseTracker.EXPENSE_CATEGORIES.get(category, {})
        
        return {
            'category': category,
            'confidence': confidence,
            'tax_deductible': cat_info.get('deductible', False),
            'deduction_percentage': cat_info.get('deduction_pct', 0),
            'suggested_subcategory': None,
            'needs_review': confidence < 0.75
        }
    
    @staticmethod
    def create_expense(merchant: str, description: str, amount: float,
                      date: datetime = None, payment_method: str = 'card',
                      manual_category: str = None) -> Dict[str, Any]:
        """
        Create a new expense with auto-categorization
        
        Args:
            merchant: Merchant name
            description: Expense description
            amount: Amount spent
            date: Transaction date (defaults to now)
            payment_method: Payment method
            manual_category: Override auto-categorization
            
        Returns:
            dict: Created expense
        """
        if date is None:
            date = datetime.now()
        
        # Auto-categorize if not manually specified
        if manual_category:
            cat_info = ExpenseTracker.EXPENSE_CATEGORIES.get(manual_category, {})
            category = manual_category
            tax_deductible = cat_info.get('deductible', False)
            deduction_pct = cat_info.get('deduction_pct', 0)
        else:
            categorization = ExpenseTracker.auto_categorize_expense(merchant, description, amount)
            category = categorization['category']
            tax_deductible = categorization['tax_deductible']
            deduction_pct = categorization['deduction_percentage']
        
        expense = Expense(
            expense_id="exp_" + ''.join(random.choices('0123456789ABCDEF', k=16)),
            date=date,
            merchant=merchant,
            description=description,
            amount=amount,
            category=category,
            subcategory=None,
            payment_method=payment_method,
            tax_deductible=tax_deductible,
            deduction_percentage=deduction_pct,
            receipt_url=None,
            notes="",
            synced_to_accounting=False
        )
        
        return asdict(expense)
    
    @staticmethod
    def capture_receipt(expense_id: str, receipt_image: Any) -> Dict[str, Any]:
        """
        Capture and OCR receipt (simulated)
        
        Args:
            expense_id: Expense to attach receipt to
            receipt_image: Receipt image file
            
        Returns:
            dict: Receipt processing result
        """
        # Simulate OCR processing
        receipt_url = f"https://receipts.pulsetrade.com/{expense_id}.pdf"
        
        # Simulate extracted data
        extracted_data = {
            'merchant': random.choice(['Staples', 'Amazon', 'Adobe', 'Starbucks']),
            'date': datetime.now() - timedelta(days=random.randint(0, 7)),
            'total': random.uniform(20, 500),
            'tax': 0,
            'items': []
        }
        
        return {
            'expense_id': expense_id,
            'receipt_url': receipt_url,
            'status': 'processed',
            'ocr_confidence': random.uniform(0.85, 0.99),
            'extracted_data': extracted_data,
            'processed_at': datetime.now(),
            'storage': 'secure_cloud'
        }
    
    @staticmethod
    def sync_to_accounting(expenses: List[Dict[str, Any]], 
                          platform: str = 'quickbooks') -> Dict[str, Any]:
        """
        Sync expenses to accounting platform
        
        Args:
            expenses: List of expenses to sync
            platform: Accounting platform (quickbooks, xero, freshbooks)
            
        Returns:
            dict: Sync result
        """
        sync_id = "sync_" + ''.join(random.choices('0123456789ABCDEF', k=12))
        
        # Simulate sync
        successful = len(expenses) - random.randint(0, max(0, len(expenses) // 20))  # 95% success rate
        failed = len(expenses) - successful
        
        return {
            'sync_id': sync_id,
            'platform': platform,
            'status': 'completed' if failed == 0 else 'partial',
            'synced_at': datetime.now(),
            'total_expenses': len(expenses),
            'successful': successful,
            'failed': failed,
            'duplicate_detected': random.randint(0, 2),
            'errors': [] if failed == 0 else [
                {'expense_id': expenses[i].get('expense_id'), 'error': 'Duplicate transaction'}
                for i in random.sample(range(len(expenses)), min(failed, len(expenses)))
            ]
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_spending_analytics(expenses_df: pd.DataFrame, 
                              period_days: int = 30) -> Dict[str, Any]:
        """
        Get spending analytics and insights
        
        Args:
            expenses_df: DataFrame of expenses
            period_days: Analysis period
            
        Returns:
            dict: Spending analytics
        """
        if expenses_df.empty:
            return {
                'total_spent': 0,
                'avg_daily': 0,
                'category_breakdown': {},
                'trends': {}
            }
        
        # Filter to period
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent = expenses_df[expenses_df['date'] >= cutoff_date]
        
        total_spent = recent['amount'].sum()
        avg_daily = total_spent / period_days
        
        # Category breakdown
        category_breakdown = recent.groupby('category')['amount'].sum().to_dict()
        
        # Tax deductible breakdown
        deductible = recent[recent['tax_deductible'] == True]['amount'].sum()
        non_deductible = total_spent - deductible
        
        # Trends
        # Compare to previous period
        prev_cutoff = cutoff_date - timedelta(days=period_days)
        previous = expenses_df[(expenses_df['date'] >= prev_cutoff) & (expenses_df['date'] < cutoff_date)]
        prev_total = previous['amount'].sum()
        
        change_pct = ((total_spent - prev_total) / prev_total * 100) if prev_total > 0 else 0
        
        return {
            'period_days': period_days,
            'total_spent': total_spent,
            'avg_daily': avg_daily,
            'monthly_projection': avg_daily * 30,
            'category_breakdown': category_breakdown,
            'top_category': max(category_breakdown.items(), key=lambda x: x[1])[0] if category_breakdown else None,
            'tax_deductible': {
                'deductible': deductible,
                'non_deductible': non_deductible,
                'deductible_pct': (deductible / total_spent * 100) if total_spent > 0 else 0
            },
            'trends': {
                'vs_previous_period': f"{'+' if change_pct > 0 else ''}{change_pct:.1f}%",
                'direction': 'up' if change_pct > 0 else 'down' if change_pct < 0 else 'flat'
            }
        }
    
    @staticmethod
    def get_category_budget_status(expenses_df: pd.DataFrame,
                                   budgets: Dict[str, float],
                                   period: str = 'monthly') -> List[Dict[str, Any]]:
        """
        Check budget status by category
        
        Args:
            expenses_df: DataFrame of expenses
            budgets: Category budgets {category: amount}
            period: Budget period ('weekly', 'monthly', 'quarterly')
            
        Returns:
            list: Budget status by category
        """
        # Determine period days
        period_days = {
            'weekly': 7,
            'monthly': 30,
            'quarterly': 90
        }.get(period, 30)
        
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent = expenses_df[expenses_df['date'] >= cutoff_date]
        
        status_list = []
        
        for category, budget in budgets.items():
            category_expenses = recent[recent['category'] == category]
            spent = category_expenses['amount'].sum()
            remaining = budget - spent
            pct_used = (spent / budget * 100) if budget > 0 else 0
            
            if pct_used >= 100:
                status = 'over_budget'
                alert = 'danger'
            elif pct_used >= 80:
                status = 'warning'
                alert = 'warning'
            elif pct_used >= 50:
                status = 'on_track'
                alert = 'success'
            else:
                status = 'well_under'
                alert = 'info'
            
            status_list.append({
                'category': category,
                'budget': budget,
                'spent': spent,
                'remaining': remaining,
                'percent_used': pct_used,
                'status': status,
                'alert_level': alert,
                'transaction_count': len(category_expenses)
            })
        
        return sorted(status_list, key=lambda x: x['percent_used'], reverse=True)
    
    @staticmethod
    def find_duplicate_expenses(expenses_df: pd.DataFrame,
                               threshold_minutes: int = 5) -> List[Dict[str, Any]]:
        """
        Find potential duplicate expenses
        
        Args:
            expenses_df: DataFrame of expenses
            threshold_minutes: Time window to consider duplicates
            
        Returns:
            list: Potential duplicate pairs
        """
        duplicates = []
        
        # Sort by date
        sorted_df = expenses_df.sort_values('date')
        
        for i in range(len(sorted_df) - 1):
            row1 = sorted_df.iloc[i]
            row2 = sorted_df.iloc[i + 1]
            
            # Check if amounts match
            if abs(row1['amount'] - row2['amount']) < 0.01:
                # Check if times are close
                time_diff = abs((row2['date'] - row1['date']).total_seconds() / 60)
                
                if time_diff <= threshold_minutes:
                    # Check if merchants are similar
                    if row1['merchant'] == row2['merchant'] or \
                       row1['merchant'].lower() in row2['merchant'].lower() or \
                       row2['merchant'].lower() in row1['merchant'].lower():
                        
                        duplicates.append({
                            'expense_1_id': row1.get('expense_id'),
                            'expense_2_id': row2.get('expense_id'),
                            'merchant': row1['merchant'],
                            'amount': row1['amount'],
                            'time_diff_minutes': time_diff,
                            'confidence': 0.9 if time_diff < 1 else 0.7
                        })
        
        return duplicates
    
    @staticmethod
    def export_for_taxes(expenses_df: pd.DataFrame, 
                        year: int = None,
                        format: str = 'csv') -> Dict[str, Any]:
        """
        Export expenses for tax filing
        
        Args:
            expenses_df: DataFrame of expenses
            year: Tax year (defaults to current)
            format: Export format
            
        Returns:
            dict: Export details
        """
        if year is None:
            year = datetime.now().year
        
        # Filter to tax year
        year_expenses = expenses_df[
            (expenses_df['date'] >= datetime(year, 1, 1)) &
            (expenses_df['date'] <= datetime(year, 12, 31))
        ]
        
        # Calculate totals
        total_expenses = year_expenses['amount'].sum()
        deductible_expenses = year_expenses[year_expenses['tax_deductible'] == True]['amount'].sum()
        
        export_id = "tax_export_" + ''.join(random.choices('0123456789', k=12))
        
        return {
            'export_id': export_id,
            'tax_year': year,
            'format': format,
            'total_expenses': total_expenses,
            'deductible_expenses': deductible_expenses,
            'expense_count': len(year_expenses),
            'by_category': year_expenses.groupby('category')['amount'].sum().to_dict(),
            'file_url': f"https://exports.pulsetrade.com/{export_id}.{format}",
            'generated_at': datetime.now(),
            'includes_receipts': True
        }

