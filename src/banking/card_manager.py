"""
Card Management Module
Handles virtual and physical card operations, controls, and security
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import streamlit as st
from dataclasses import dataclass, asdict

@dataclass
class Card:
    """Debit card (virtual or physical)"""
    card_id: str
    card_number: str
    cvv: str
    expiry_date: str
    cardholder_name: str
    card_type: str  # 'virtual', 'physical'
    status: str  # 'active', 'frozen', 'cancelled', 'lost', 'stolen'
    network: str  # 'visa', 'mastercard'
    daily_limit: float
    monthly_limit: float
    current_daily_spend: float
    current_monthly_spend: float
    blocked_categories: List[str]
    allowed_countries: List[str]
    supports_contactless: bool
    supports_online: bool
    supports_apple_pay: bool
    supports_google_pay: bool

class CardManager:
    """Manages card operations and controls"""
    
    # Merchant Category Codes (MCCs) for restrictions
    MCC_CATEGORIES = {
        'gambling': ['7995', '7802', '7800'],
        'adult_entertainment': ['5967'],
        'alcohol': ['5921', '5813'],
        'cash_advance': ['6011', '6010'],
        'cryptocurrency': ['6051'],
        'gaming': ['7994'],
        'money_transfer': ['4829', '6051']
    }
    
    @staticmethod
    @st.cache_data
    def create_virtual_card(account_id: str, cardholder_name: str,
                           daily_limit: float = 5000.0,
                           monthly_limit: float = 50000.0) -> Dict[str, Any]:
        """
        Create a new virtual card instantly
        
        Args:
            account_id: Account to link card to
            cardholder_name: Name on card
            daily_limit: Daily spending limit
            monthly_limit: Monthly spending limit
            
        Returns:
            dict: Virtual card details
        """
        card_id = "card_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        
        # Generate Visa card number
        card_number = '4' + ''.join(random.choices('0123456789', k=15))
        
        card = Card(
            card_id=card_id,
            card_number=card_number,
            cvv=''.join(random.choices('0123456789', k=3)),
            expiry_date=(datetime.now() + timedelta(days=1095)).strftime('%m/%y'),
            cardholder_name=cardholder_name.upper(),
            card_type='virtual',
            status='active',
            network='visa',
            daily_limit=daily_limit,
            monthly_limit=monthly_limit,
            current_daily_spend=0.0,
            current_monthly_spend=0.0,
            blocked_categories=[],
            allowed_countries=['US'],
            supports_contactless=False,
            supports_online=True,
            supports_apple_pay=True,
            supports_google_pay=True
        )
        
        return {
            **asdict(card),
            'account_id': account_id,
            'issued_at': datetime.now(),
            'instant_issuance': True,
            'add_to_wallet': {
                'apple_pay': True,
                'google_pay': True,
                'samsung_pay': False
            }
        }
    
    @staticmethod
    def order_physical_card(account_id: str, cardholder_name: str,
                          shipping_address: Dict[str, str],
                          expedited: bool = False) -> Dict[str, Any]:
        """
        Order a physical debit card
        
        Args:
            account_id: Account to link card to
            cardholder_name: Name on card
            shipping_address: Delivery address
            expedited: Rush shipping (additional fee)
            
        Returns:
            dict: Physical card order details
        """
        order_id = "order_" + ''.join(random.choices('0123456789', k=12))
        
        # Delivery time
        if expedited:
            delivery_days = random.randint(2, 3)
            shipping_fee = 25.0
        else:
            delivery_days = random.randint(5, 7)
            shipping_fee = 0.0
        
        return {
            'order_id': order_id,
            'account_id': account_id,
            'card_type': 'physical',
            'cardholder_name': cardholder_name,
            'status': 'ordered',
            'ordered_at': datetime.now(),
            'estimated_delivery': datetime.now() + timedelta(days=delivery_days),
            'shipping_address': shipping_address,
            'shipping_method': 'FedEx Express' if expedited else 'USPS Priority Mail',
            'shipping_fee': shipping_fee,
            'tracking_number': None,  # Assigned when shipped
            'activation_required': True
        }
    
    @staticmethod
    def get_card_details(card_id: str) -> Dict[str, Any]:
        """Get full card details"""
        # In real app, fetch from database
        # For demo, generate realistic data
        
        return {
            'card_id': card_id,
            'last_four': ''.join(random.choices('0123456789', k=4)),
            'network': 'Visa',
            'type': random.choice(['virtual', 'physical']),
            'status': 'active',
            'expires': (datetime.now() + timedelta(days=random.randint(365, 1095))).strftime('%m/%y'),
            'daily_limit': 5000.0,
            'monthly_limit': 50000.0,
            'current_daily_spend': random.uniform(0, 1000),
            'current_monthly_spend': random.uniform(0, 5000)
        }
    
    @staticmethod
    def freeze_card(card_id: str, reason: str = 'user_requested') -> Dict[str, Any]:
        """
        Freeze a card to prevent all transactions
        
        Args:
            card_id: Card to freeze
            reason: Freeze reason
            
        Returns:
            dict: Freeze confirmation
        """
        return {
            'card_id': card_id,
            'previous_status': 'active',
            'new_status': 'frozen',
            'frozen_at': datetime.now(),
            'reason': reason,
            'reversible': True,
            'transactions_blocked': True
        }
    
    @staticmethod
    def unfreeze_card(card_id: str) -> Dict[str, Any]:
        """
        Unfreeze a card to allow transactions
        
        Args:
            card_id: Card to unfreeze
            
        Returns:
            dict: Unfreeze confirmation
        """
        return {
            'card_id': card_id,
            'previous_status': 'frozen',
            'new_status': 'active',
            'unfrozen_at': datetime.now(),
            'transactions_enabled': True
        }
    
    @staticmethod
    def set_spending_limits(card_id: str, daily_limit: float = None,
                          monthly_limit: float = None) -> Dict[str, Any]:
        """
        Update card spending limits
        
        Args:
            card_id: Card identifier
            daily_limit: New daily limit (optional)
            monthly_limit: New monthly limit (optional)
            
        Returns:
            dict: Updated limits
        """
        return {
            'card_id': card_id,
            'previous_limits': {
                'daily': 5000.0,
                'monthly': 50000.0
            },
            'new_limits': {
                'daily': daily_limit or 5000.0,
                'monthly': monthly_limit or 50000.0
            },
            'updated_at': datetime.now(),
            'effective_immediately': True
        }
    
    @staticmethod
    def set_merchant_controls(card_id: str, 
                            block_categories: List[str] = None,
                            allow_only_countries: List[str] = None,
                            allow_online: bool = True,
                            allow_contactless: bool = True) -> Dict[str, Any]:
        """
        Set merchant and transaction type controls
        
        Args:
            card_id: Card identifier
            block_categories: Merchant categories to block (e.g., ['gambling', 'alcohol'])
            allow_only_countries: Countries where card can be used
            allow_online: Allow online transactions
            allow_contactless: Allow contactless payments
            
        Returns:
            dict: Updated controls
        """
        blocked_mccs = []
        if block_categories:
            for category in block_categories:
                blocked_mccs.extend(CardManager.MCC_CATEGORIES.get(category, []))
        
        return {
            'card_id': card_id,
            'controls': {
                'blocked_categories': block_categories or [],
                'blocked_mccs': blocked_mccs,
                'allowed_countries': allow_only_countries or ['US'],
                'online_transactions': allow_online,
                'contactless_transactions': allow_contactless,
                'international_transactions': len(allow_only_countries or ['US']) > 1
            },
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def report_lost_stolen(card_id: str, reason: str) -> Dict[str, Any]:
        """
        Report card as lost or stolen and issue replacement
        
        Args:
            card_id: Card identifier
            reason: 'lost' or 'stolen'
            
        Returns:
            dict: Report confirmation and replacement details
        """
        new_card_id = "card_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        
        return {
            'old_card_id': card_id,
            'old_card_status': reason,
            'reported_at': datetime.now(),
            'transactions_blocked': True,
            'replacement_card': {
                'card_id': new_card_id,
                'status': 'pending_issuance',
                'expected_delivery': datetime.now() + timedelta(days=random.randint(3, 5)),
                'expedited_available': True
            },
            'fraud_protection': {
                'liability_waived': True,
                'zero_liability': True,
                'investigation_status': 'opened' if reason == 'stolen' else None
            }
        }
    
    @staticmethod
    def get_card_transactions(card_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get card transaction history
        
        Args:
            card_id: Card identifier
            days: Number of days of history
            
        Returns:
            list: Recent transactions
        """
        transactions = []
        
        merchants = [
            {'name': 'Amazon.com', 'category': 'Shopping', 'mcc': '5942'},
            {'name': 'Starbucks', 'category': 'Food & Drink', 'mcc': '5814'},
            {'name': 'Adobe Creative Cloud', 'category': 'Software', 'mcc': '5734'},
            {'name': 'Google Workspace', 'category': 'Software', 'mcc': '5734'},
            {'name': 'Uber', 'category': 'Transportation', 'mcc': '4121'},
            {'name': 'Shell Gas', 'category': 'Gas', 'mcc': '5541'},
            {'name': 'Target', 'category': 'Shopping', 'mcc': '5411'},
            {'name': 'LinkedIn Premium', 'category': 'Software', 'mcc': '5734'},
            {'name': 'AWS', 'category': 'Software', 'mcc': '5734'},
            {'name': 'Whole Foods', 'category': 'Groceries', 'mcc': '5411'}
        ]
        
        for i in range(random.randint(10, 25)):
            merchant = random.choice(merchants)
            amount = random.uniform(5, 500)
            
            # Round to 2 decimals for common amounts, but keep some exact amounts
            if random.random() < 0.7:
                amount = round(amount, 2)
            
            transactions.append({
                'transaction_id': f"txn_{i:08d}",
                'card_id': card_id,
                'date': datetime.now() - timedelta(days=random.randint(0, days), 
                                                  hours=random.randint(0, 23),
                                                  minutes=random.randint(0, 59)),
                'merchant': merchant['name'],
                'amount': amount,
                'category': merchant['category'],
                'mcc': merchant['mcc'],
                'status': random.choice(['completed'] * 9 + ['pending']),
                'transaction_type': random.choice(['purchase'] * 8 + ['refund'] * 2),
                'location': random.choice(['Online', 'In-Store']),
                'declined': False
            })
        
        # Sort by date descending
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        return transactions
    
    @staticmethod
    def get_spending_analytics(card_id: str, period_days: int = 30) -> Dict[str, Any]:
        """
        Get spending analytics and insights for a card
        
        Args:
            card_id: Card identifier
            period_days: Analysis period in days
            
        Returns:
            dict: Spending analytics
        """
        transactions = CardManager.get_card_transactions(card_id, period_days)
        
        # Calculate metrics
        total_spent = sum(t['amount'] for t in transactions if t['transaction_type'] == 'purchase')
        total_refunds = sum(t['amount'] for t in transactions if t['transaction_type'] == 'refund')
        net_spent = total_spent - total_refunds
        
        # Category breakdown
        category_spending = {}
        for t in transactions:
            if t['transaction_type'] == 'purchase':
                category = t['category']
                category_spending[category] = category_spending.get(category, 0) + t['amount']
        
        # Top merchants
        merchant_spending = {}
        for t in transactions:
            if t['transaction_type'] == 'purchase':
                merchant = t['merchant']
                merchant_spending[merchant] = merchant_spending.get(merchant, 0) + t['amount']
        
        top_merchants = sorted(merchant_spending.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'card_id': card_id,
            'period_days': period_days,
            'summary': {
                'total_transactions': len(transactions),
                'total_spent': total_spent,
                'total_refunds': total_refunds,
                'net_spent': net_spent,
                'avg_transaction': net_spent / len(transactions) if transactions else 0,
                'largest_transaction': max((t['amount'] for t in transactions), default=0)
            },
            'category_breakdown': category_spending,
            'top_merchants': [{'name': m[0], 'amount': m[1]} for m in top_merchants],
            'trends': {
                'vs_previous_period': random.choice(['+', '-']) + f"{random.uniform(5, 25):.1f}%",
                'monthly_projection': net_spent / period_days * 30
            }
        }

