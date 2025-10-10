"""
Account Management Module
Handles bank accounts, KYC, account creation, and balance management
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import streamlit as st
from dataclasses import dataclass, asdict

@dataclass
class VirtualCard:
    """Virtual debit card"""
    card_id: str
    card_number: str
    cvv: str
    expiry_date: str
    cardholder_name: str
    status: str  # 'active', 'frozen', 'cancelled'
    spending_limit_daily: float
    spending_limit_monthly: float
    merchant_restrictions: List[str]

class AccountManager:
    """Manages bank accounts and related operations"""
    
    @staticmethod
    @st.cache_data
    def create_account(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate instant account creation after KYC
        
        Args:
            user_data: User information (name, email, SSN, address, etc.)
            
        Returns:
            dict: Account details including account number, routing number
        """
        account_id = "acc_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        account_number = ''.join(random.choices('0123456789', k=12))
        routing_number = '051000017'  # Chase routing number (demo)
        
        return {
            'account_id': account_id,
            'account_number': account_number,
            'routing_number': routing_number,
            'account_type': 'checking',
            'status': 'active',
            'created_at': datetime.now(),
            'balance': 0.0,
            'available_balance': 0.0,
            'currency': 'USD',
            'user_name': user_data.get('name', 'PulseTrade User'),
            'user_email': user_data.get('email', 'user@example.com')
        }
    
    @staticmethod
    @st.cache_data
    def simulate_kyc_flow(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate KYC (Know Your Customer) verification flow
        
        Args:
            user_data: User information for verification
            
        Returns:
            dict: KYC result with status and details
        """
        # Simulate processing time
        # In real app, this would involve document verification, ID check, etc.
        
        # 95% approval rate for demo
        approved = random.random() < 0.95
        
        if approved:
            return {
                'status': 'approved',
                'verified_at': datetime.now(),
                'verification_method': 'document_upload',
                'identity_confirmed': True,
                'address_confirmed': True,
                'sanctions_check': 'clear',
                'pep_check': 'clear',
                'processing_time_seconds': random.uniform(30, 120),
                'next_steps': [
                    'Account creation',
                    'Virtual card issuance',
                    'Initial deposit'
                ]
            }
        else:
            return {
                'status': 'pending_review',
                'reason': 'Additional verification required',
                'required_documents': ['Government ID', 'Proof of address'],
                'estimated_review_time': '2-3 business days'
            }
    
    @staticmethod
    @st.cache_data
    def get_account_balance(account_id: str) -> Dict[str, float]:
        """
        Get account balance information
        
        Args:
            account_id: Account identifier
            
        Returns:
            dict: Current balance, available balance, pending transactions
        """
        # In real app, this would query the database
        # For demo, generate realistic balances
        
        current_balance = random.uniform(5000, 50000)
        pending_debits = random.uniform(0, 500)
        pending_credits = random.uniform(0, 2000)
        
        return {
            'current_balance': current_balance,
            'available_balance': current_balance - pending_debits,
            'pending_debits': pending_debits,
            'pending_credits': pending_credits,
            'currency': 'USD',
            'as_of': datetime.now()
        }
    
    @staticmethod
    @st.cache_data(ttl=60)
    def get_account_summary(account_id: str) -> Dict[str, Any]:
        """
        Get comprehensive account summary
        
        Args:
            account_id: Account identifier
            
        Returns:
            dict: Account summary with balances, limits, status
        """
        balance_info = AccountManager.get_account_balance(account_id)
        
        return {
            'account_id': account_id,
            'account_type': 'Business Checking',
            'status': 'active',
            'balances': balance_info,
            'limits': {
                'ach_daily': 50000,
                'ach_monthly': 500000,
                'wire_daily': 100000,
                'atm_daily': 1000,
                'debit_card_daily': 5000
            },
            'features': [
                'ACH transfers',
                'Wire transfers',
                'Virtual cards',
                'P2P payments',
                'Mobile check deposit',
                'Bill pay'
            ],
            'opened_date': datetime.now() - timedelta(days=random.randint(30, 365)),
            'last_activity': datetime.now() - timedelta(hours=random.randint(1, 48))
        }
    
    @staticmethod
    def issue_virtual_card(account_id: str, cardholder_name: str) -> Dict[str, Any]:
        """
        Issue a virtual debit card instantly
        
        Args:
            account_id: Account to link card to
            cardholder_name: Name to appear on card
            
        Returns:
            dict: Virtual card details
        """
        card = VirtualCard(
            card_id="card_" + ''.join(random.choices('0123456789ABCDEF', k=16)),
            card_number='4' + ''.join(random.choices('0123456789', k=15)),  # Visa
            cvv=''.join(random.choices('0123456789', k=3)),
            expiry_date=(datetime.now() + timedelta(days=1095)).strftime('%m/%y'),  # 3 years
            cardholder_name=cardholder_name.upper(),
            status='active',
            spending_limit_daily=5000.0,
            spending_limit_monthly=50000.0,
            merchant_restrictions=[]
        )
        
        return {
            **asdict(card),
            'account_id': account_id,
            'card_type': 'virtual',
            'issued_at': datetime.now(),
            'supports_apple_pay': True,
            'supports_google_pay': True
        }
    
    @staticmethod
    def order_physical_card(account_id: str, shipping_address: Dict[str, str]) -> Dict[str, Any]:
        """
        Order a physical debit card
        
        Args:
            account_id: Account to link card to
            shipping_address: Shipping address details
            
        Returns:
            dict: Order confirmation
        """
        return {
            'order_id': "order_" + ''.join(random.choices('0123456789', k=12)),
            'card_type': 'physical',
            'status': 'ordered',
            'ordered_at': datetime.now(),
            'estimated_delivery': datetime.now() + timedelta(days=random.randint(5, 7)),
            'shipping_address': shipping_address,
            'shipping_method': 'USPS Priority Mail',
            'tracking_number': None  # Assigned when shipped
        }
    
    @staticmethod
    def freeze_card(card_id: str) -> Dict[str, Any]:
        """Freeze a card to prevent transactions"""
        return {
            'card_id': card_id,
            'previous_status': 'active',
            'new_status': 'frozen',
            'frozen_at': datetime.now(),
            'reason': 'user_requested'
        }
    
    @staticmethod
    def unfreeze_card(card_id: str) -> Dict[str, Any]:
        """Unfreeze a card to allow transactions"""
        return {
            'card_id': card_id,
            'previous_status': 'frozen',
            'new_status': 'active',
            'unfrozen_at': datetime.now()
        }
    
    @staticmethod
    def set_card_limits(card_id: str, daily_limit: float = None, 
                       monthly_limit: float = None) -> Dict[str, Any]:
        """
        Set spending limits on a card
        
        Args:
            card_id: Card identifier
            daily_limit: Daily spending limit (optional)
            monthly_limit: Monthly spending limit (optional)
            
        Returns:
            dict: Updated card limits
        """
        return {
            'card_id': card_id,
            'daily_limit': daily_limit or 5000.0,
            'monthly_limit': monthly_limit or 50000.0,
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def set_merchant_restrictions(card_id: str, 
                                  blocked_categories: List[str] = None) -> Dict[str, Any]:
        """
        Set merchant category restrictions
        
        Args:
            card_id: Card identifier
            blocked_categories: List of MCC categories to block
            
        Returns:
            dict: Updated restrictions
        """
        blocked = blocked_categories or []
        
        return {
            'card_id': card_id,
            'blocked_categories': blocked,
            'updated_at': datetime.now()
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_card_transactions(card_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get recent card transactions
        
        Args:
            card_id: Card identifier
            days: Number of days of history
            
        Returns:
            list: Recent transactions
        """
        transactions = []
        merchants = [
            "Amazon.com", "Starbucks", "Uber", "Adobe Creative Cloud",
            "Microsoft 365", "Google Workspace", "AWS", "DigitalOcean",
            "Whole Foods", "Target", "Shell Gas", "LinkedIn Premium"
        ]
        
        for i in range(random.randint(5, 15)):
            transactions.append({
                'transaction_id': f"txn_{i:08d}",
                'date': datetime.now() - timedelta(days=random.randint(0, days)),
                'merchant': random.choice(merchants),
                'amount': random.uniform(5, 500),
                'status': random.choice(['completed'] * 9 + ['pending']),
                'category': random.choice(['Shopping', 'Food', 'Software', 'Travel', 'Gas'])
            })
        
        return sorted(transactions, key=lambda x: x['date'], reverse=True)

