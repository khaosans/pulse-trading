"""
Payment Engine Module
Handles ACH, wires, P2P payments, and scheduled transfers
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import streamlit as st
from dataclasses import dataclass, asdict
from enum import Enum

class PaymentStatus(Enum):
    """Payment status types"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class PaymentType(Enum):
    """Payment method types"""
    ACH_DEBIT = "ach_debit"
    ACH_CREDIT = "ach_credit"
    WIRE = "wire"
    P2P = "p2p"
    CARD = "card"

@dataclass
class Payment:
    """Payment transaction"""
    payment_id: str
    payment_type: str
    amount: float
    from_account: str
    to_account: str
    to_name: str
    status: str
    initiated_at: datetime
    completed_at: Optional[datetime]
    description: str
    fee: float
    expected_completion: datetime

class PaymentEngine:
    """Manages all payment operations"""
    
    # ACH takes 1-3 business days
    # Wires complete same day (if before cutoff)
    # P2P is instant
    
    @staticmethod
    def initiate_ach_transfer(from_account: str, to_account: str, 
                             routing_number: str, account_number: str,
                             amount: float, description: str = "",
                             is_debit: bool = False) -> Dict[str, Any]:
        """
        Initiate an ACH transfer (push or pull)
        
        Args:
            from_account: Source account ID
            to_account: Recipient name
            routing_number: Recipient routing number
            account_number: Recipient account number
            amount: Transfer amount
            description: Transfer description
            is_debit: True for ACH pull, False for ACH push
            
        Returns:
            dict: Payment details with estimated completion
        """
        payment_id = "ach_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        
        # ACH typically takes 1-3 business days
        business_days = random.randint(1, 3)
        initiated = datetime.now()
        expected_completion = PaymentEngine._add_business_days(initiated, business_days)
        
        payment = Payment(
            payment_id=payment_id,
            payment_type=PaymentType.ACH_DEBIT.value if is_debit else PaymentType.ACH_CREDIT.value,
            amount=amount,
            from_account=from_account,
            to_account=to_account,
            to_name=to_account,
            status=PaymentStatus.PENDING.value,
            initiated_at=initiated,
            completed_at=None,
            description=description or "ACH Transfer",
            fee=0.0,  # Most ACH transfers are free
            expected_completion=expected_completion
        )
        
        return {
            **asdict(payment),
            'routing_number': routing_number[-4:],  # Last 4 digits only for security
            'account_number': account_number[-4:],
            'estimated_days': business_days,
            'cutoff_time': "5:00 PM ET",
            'cancellable_until': initiated + timedelta(hours=1)
        }
    
    @staticmethod
    def initiate_wire_transfer(from_account: str, to_account: str,
                              routing_number: str, account_number: str,
                              amount: float, description: str = "") -> Dict[str, Any]:
        """
        Initiate a wire transfer (same-day, higher fee)
        
        Args:
            from_account: Source account ID
            to_account: Recipient name
            routing_number: Recipient routing number
            account_number: Recipient account number
            amount: Transfer amount
            description: Wire description
            
        Returns:
            dict: Wire transfer details
        """
        payment_id = "wire_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        
        # Wires complete same day if before cutoff (2 PM ET)
        initiated = datetime.now()
        cutoff_hour = 14  # 2 PM
        
        if initiated.hour < cutoff_hour:
            # Same day
            expected_completion = initiated.replace(hour=17, minute=0)
        else:
            # Next business day
            expected_completion = PaymentEngine._add_business_days(initiated, 1)
            expected_completion = expected_completion.replace(hour=17, minute=0)
        
        # Wire fee
        fee = 25.0 if amount < 10000 else 35.0
        
        payment = Payment(
            payment_id=payment_id,
            payment_type=PaymentType.WIRE.value,
            amount=amount,
            from_account=from_account,
            to_account=to_account,
            to_name=to_account,
            status=PaymentStatus.PROCESSING.value,
            initiated_at=initiated,
            completed_at=None,
            description=description or "Wire Transfer",
            fee=fee,
            expected_completion=expected_completion
        )
        
        return {
            **asdict(payment),
            'routing_number': routing_number[-4:],
            'account_number': account_number[-4:],
            'cutoff_time': "2:00 PM ET",
            'same_day_eligible': initiated.hour < cutoff_hour
        }
    
    @staticmethod
    def initiate_p2p_transfer(from_account: str, to_email: str, 
                            amount: float, description: str = "") -> Dict[str, Any]:
        """
        Initiate a P2P (peer-to-peer) transfer - instant
        
        Args:
            from_account: Source account ID
            to_email: Recipient email
            amount: Transfer amount
            description: Transfer description
            
        Returns:
            dict: P2P transfer details
        """
        payment_id = "p2p_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        initiated = datetime.now()
        
        payment = Payment(
            payment_id=payment_id,
            payment_type=PaymentType.P2P.value,
            amount=amount,
            from_account=from_account,
            to_account=to_email,
            to_name=to_email.split('@')[0],
            status=PaymentStatus.COMPLETED.value,  # P2P is instant
            initiated_at=initiated,
            completed_at=initiated,
            description=description or "P2P Transfer",
            fee=0.0,  # Free P2P
            expected_completion=initiated
        )
        
        return {
            **asdict(payment),
            'recipient_email': to_email,
            'instant': True,
            'notification_sent': True
        }
    
    @staticmethod
    def schedule_recurring_payment(from_account: str, to_account: str,
                                  amount: float, frequency: str,
                                  start_date: datetime,
                                  end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Schedule a recurring payment
        
        Args:
            from_account: Source account ID
            to_account: Recipient
            amount: Payment amount
            frequency: 'daily', 'weekly', 'biweekly', 'monthly', 'quarterly'
            start_date: First payment date
            end_date: Optional end date
            
        Returns:
            dict: Scheduled payment details
        """
        schedule_id = "sched_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        
        # Calculate next occurrences
        next_dates = PaymentEngine._calculate_next_occurrences(start_date, frequency, count=12)
        
        return {
            'schedule_id': schedule_id,
            'from_account': from_account,
            'to_account': to_account,
            'amount': amount,
            'frequency': frequency,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'active',
            'next_payment': next_dates[0] if next_dates else None,
            'upcoming_payments': next_dates[:5],
            'total_scheduled': len(next_dates),
            'created_at': datetime.now()
        }
    
    @staticmethod
    def get_payment_status(payment_id: str) -> Dict[str, Any]:
        """
        Get current status of a payment
        
        Args:
            payment_id: Payment identifier
            
        Returns:
            dict: Payment status and details
        """
        # Simulate status checking
        payment_type = payment_id.split('_')[0]
        
        if payment_type == 'p2p':
            status = PaymentStatus.COMPLETED.value
            completed_at = datetime.now()
        elif payment_type == 'wire':
            # 80% completed, 15% processing, 5% pending
            status = random.choices(
                [PaymentStatus.COMPLETED.value, PaymentStatus.PROCESSING.value, PaymentStatus.PENDING.value],
                weights=[80, 15, 5]
            )[0]
            completed_at = datetime.now() if status == PaymentStatus.COMPLETED.value else None
        else:  # ACH
            # 60% completed, 30% processing, 10% pending
            status = random.choices(
                [PaymentStatus.COMPLETED.value, PaymentStatus.PROCESSING.value, PaymentStatus.PENDING.value],
                weights=[60, 30, 10]
            )[0]
            completed_at = datetime.now() if status == PaymentStatus.COMPLETED.value else None
        
        return {
            'payment_id': payment_id,
            'status': status,
            'completed_at': completed_at,
            'checked_at': datetime.now()
        }
    
    @staticmethod
    def cancel_payment(payment_id: str) -> Dict[str, Any]:
        """
        Cancel a pending payment (if still cancellable)
        
        Args:
            payment_id: Payment identifier
            
        Returns:
            dict: Cancellation result
        """
        # Check if payment can be cancelled
        # ACH can be cancelled within 1 hour
        # Wires cannot be cancelled once initiated
        # P2P cannot be cancelled (instant)
        
        payment_type = payment_id.split('_')[0]
        
        if payment_type == 'p2p':
            return {
                'success': False,
                'reason': 'P2P payments are instant and cannot be cancelled',
                'payment_id': payment_id
            }
        elif payment_type == 'wire':
            return {
                'success': False,
                'reason': 'Wire transfers cannot be cancelled once initiated',
                'payment_id': payment_id
            }
        else:  # ACH
            # Simulate cancellation window
            can_cancel = random.random() < 0.7  # 70% within cancellation window
            
            if can_cancel:
                return {
                    'success': True,
                    'status': PaymentStatus.CANCELLED.value,
                    'cancelled_at': datetime.now(),
                    'payment_id': payment_id
                }
            else:
                return {
                    'success': False,
                    'reason': 'Payment has already been submitted for processing',
                    'payment_id': payment_id
                }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_payment_history(account_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get payment history for an account
        
        Args:
            account_id: Account identifier
            days: Number of days of history
            
        Returns:
            list: Payment history
        """
        from src.utils.data_generator import DataGenerator
        
        # Generate realistic payment history
        transactions_df = DataGenerator.generate_transactions(days)
        
        payments = []
        for _, row in transactions_df.iterrows():
            payments.append({
                'payment_id': row['transaction_id'],
                'date': row['date'],
                'description': row['description'],
                'amount': row['amount'],
                'type': 'credit' if row['transaction_type'] == 'credit' else 'debit',
                'status': row['status'],
                'category': row['category']
            })
        
        return payments
    
    @staticmethod
    def _add_business_days(start_date: datetime, days: int) -> datetime:
        """Add business days to a date, skipping weekends"""
        current = start_date
        days_added = 0
        
        while days_added < days:
            current += timedelta(days=1)
            # Skip weekends (Saturday=5, Sunday=6)
            if current.weekday() < 5:
                days_added += 1
        
        return current
    
    @staticmethod
    def _calculate_next_occurrences(start_date: datetime, frequency: str, 
                                   count: int = 12) -> List[datetime]:
        """Calculate next N occurrences of a recurring payment"""
        occurrences = []
        current = start_date
        
        frequency_map = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'biweekly': timedelta(weeks=2),
            'monthly': None,  # Handle separately
            'quarterly': None  # Handle separately
        }
        
        for i in range(count):
            occurrences.append(current)
            
            if frequency in ['daily', 'weekly', 'biweekly']:
                current += frequency_map[frequency]
            elif frequency == 'monthly':
                # Add one month (approximately)
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
            elif frequency == 'quarterly':
                # Add 3 months
                month = current.month + 3
                year = current.year
                if month > 12:
                    month -= 12
                    year += 1
                current = current.replace(year=year, month=month)
        
        return occurrences

