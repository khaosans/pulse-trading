"""
Invoice Engine Module
Handles invoice creation, tracking, payments, and client management
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import streamlit as st
from dataclasses import dataclass, asdict
import pandas as pd

@dataclass
class InvoiceLineItem:
    """Single line item on an invoice"""
    description: str
    quantity: float
    unit_price: float
    amount: float

@dataclass
class Invoice:
    """Complete invoice"""
    invoice_id: str
    invoice_number: str
    client_id: str
    client_name: str
    client_email: str
    issue_date: datetime
    due_date: datetime
    line_items: List[InvoiceLineItem]
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount: float
    total_amount: float
    status: str  # 'draft', 'sent', 'viewed', 'paid', 'overdue', 'cancelled'
    payment_date: Optional[datetime]
    payment_method: Optional[str]
    notes: str
    payment_link: str

class InvoiceEngine:
    """Manages invoicing and collections"""
    
    PAYMENT_TERMS = {
        'net_15': 15,
        'net_30': 30,
        'net_45': 45,
        'net_60': 60,
        'due_on_receipt': 0
    }
    
    @staticmethod
    def create_invoice(client_id: str, client_name: str, client_email: str,
                      line_items: List[Dict[str, Any]], 
                      payment_terms: str = 'net_30',
                      tax_rate: float = 0.0,
                      discount: float = 0.0,
                      notes: str = "") -> Dict[str, Any]:
        """
        Create a new invoice
        
        Args:
            client_id: Client identifier
            client_name: Client name
            client_email: Client email
            line_items: List of line items with description, quantity, unit_price
            payment_terms: Payment terms (net_15, net_30, etc.)
            tax_rate: Tax rate (e.g., 0.08 for 8%)
            discount: Discount amount
            notes: Invoice notes
            
        Returns:
            dict: Created invoice
        """
        invoice_id = "inv_" + ''.join(random.choices('0123456789ABCDEF', k=16))
        invoice_number = f"INV-{random.randint(1000, 9999)}"
        
        issue_date = datetime.now()
        due_days = InvoiceEngine.PAYMENT_TERMS.get(payment_terms, 30)
        due_date = issue_date + timedelta(days=due_days)
        
        # Calculate totals
        items = []
        subtotal = 0.0
        
        for item in line_items:
            amount = item['quantity'] * item['unit_price']
            items.append(InvoiceLineItem(
                description=item['description'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                amount=amount
            ))
            subtotal += amount
        
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount - discount
        
        # Generate payment link
        payment_link = f"https://pay.pulsetrade.com/{invoice_id}"
        
        invoice = Invoice(
            invoice_id=invoice_id,
            invoice_number=invoice_number,
            client_id=client_id,
            client_name=client_name,
            client_email=client_email,
            issue_date=issue_date,
            due_date=due_date,
            line_items=items,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            discount=discount,
            total_amount=total,
            status='draft',
            payment_date=None,
            payment_method=None,
            notes=notes,
            payment_link=payment_link
        )
        
        return {
            **asdict(invoice),
            'line_items': [asdict(item) for item in items],
            'created_at': datetime.now()
        }
    
    @staticmethod
    def send_invoice(invoice_id: str, method: str = 'email') -> Dict[str, Any]:
        """
        Send invoice to client
        
        Args:
            invoice_id: Invoice identifier
            method: Delivery method ('email', 'link')
            
        Returns:
            dict: Send confirmation
        """
        return {
            'invoice_id': invoice_id,
            'status': 'sent',
            'sent_at': datetime.now(),
            'delivery_method': method,
            'recipient_notified': True,
            'payment_link_active': True,
            'tracking_enabled': True
        }
    
    @staticmethod
    def track_invoice_status(invoice_id: str) -> Dict[str, Any]:
        """
        Track invoice status and viewing activity
        
        Args:
            invoice_id: Invoice identifier
            
        Returns:
            dict: Invoice tracking data
        """
        # Simulate tracking data
        statuses = ['sent', 'viewed', 'paid', 'overdue']
        weights = [30, 40, 20, 10]
        status = random.choices(statuses, weights=weights)[0]
        
        sent_at = datetime.now() - timedelta(days=random.randint(1, 30))
        viewed_at = sent_at + timedelta(hours=random.randint(2, 72)) if status != 'sent' else None
        paid_at = viewed_at + timedelta(days=random.randint(1, 14)) if status == 'paid' else None
        
        return {
            'invoice_id': invoice_id,
            'status': status,
            'sent_at': sent_at,
            'viewed_at': viewed_at,
            'view_count': random.randint(1, 5) if viewed_at else 0,
            'paid_at': paid_at,
            'days_outstanding': (datetime.now() - sent_at).days,
            'reminders_sent': random.randint(0, 3) if status in ['sent', 'viewed', 'overdue'] else 0
        }
    
    @staticmethod
    def mark_as_paid(invoice_id: str, payment_method: str, 
                    payment_date: datetime = None) -> Dict[str, Any]:
        """
        Mark invoice as paid
        
        Args:
            invoice_id: Invoice identifier
            payment_method: How payment was received ('ach', 'card', 'wire', 'check')
            payment_date: Payment date (defaults to now)
            
        Returns:
            dict: Payment confirmation
        """
        if payment_date is None:
            payment_date = datetime.now()
        
        return {
            'invoice_id': invoice_id,
            'previous_status': 'sent',
            'new_status': 'paid',
            'payment_date': payment_date,
            'payment_method': payment_method,
            'auto_reconciled': True,
            'client_notified': True
        }
    
    @staticmethod
    def send_reminder(invoice_id: str, reminder_type: str = 'friendly') -> Dict[str, Any]:
        """
        Send payment reminder to client
        
        Args:
            invoice_id: Invoice identifier
            reminder_type: 'friendly', 'firm', 'final'
            
        Returns:
            dict: Reminder confirmation
        """
        templates = {
            'friendly': "Just a friendly reminder that Invoice {invoice_number} is due.",
            'firm': "This is a reminder that Invoice {invoice_number} is now overdue.",
            'final': "FINAL NOTICE: Invoice {invoice_number} is seriously overdue."
        }
        
        return {
            'invoice_id': invoice_id,
            'reminder_type': reminder_type,
            'sent_at': datetime.now(),
            'template_used': templates.get(reminder_type),
            'delivery_method': 'email',
            'delivered': True
        }
    
    @staticmethod
    def apply_late_fee(invoice_id: str, fee_amount: float = None,
                      fee_percentage: float = None) -> Dict[str, Any]:
        """
        Apply late fee to overdue invoice
        
        Args:
            invoice_id: Invoice identifier
            fee_amount: Fixed late fee amount
            fee_percentage: Late fee as percentage of total
            
        Returns:
            dict: Updated invoice with late fee
        """
        # In real app, fetch invoice and calculate
        original_total = random.uniform(1000, 5000)
        
        if fee_percentage:
            late_fee = original_total * (fee_percentage / 100)
        else:
            late_fee = fee_amount or 50.0
        
        new_total = original_total + late_fee
        
        return {
            'invoice_id': invoice_id,
            'original_total': original_total,
            'late_fee': late_fee,
            'new_total': new_total,
            'applied_at': datetime.now(),
            'client_notified': True
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def calculate_dso(invoices: List[Dict[str, Any]]) -> float:
        """
        Calculate Days Sales Outstanding (DSO)
        Average number of days to collect payment
        
        Args:
            invoices: List of invoice dictionaries
            
        Returns:
            float: Average DSO in days
        """
        paid_invoices = [inv for inv in invoices if inv.get('status') == 'paid' 
                        and inv.get('payment_date') and inv.get('issue_date')]
        
        if not paid_invoices:
            return 0.0
        
        total_days = 0
        for inv in paid_invoices:
            issue = inv['issue_date'] if isinstance(inv['issue_date'], datetime) else datetime.fromisoformat(str(inv['issue_date']))
            paid = inv['payment_date'] if isinstance(inv['payment_date'], datetime) else datetime.fromisoformat(str(inv['payment_date']))
            days = (paid - issue).days
            total_days += days
        
        return total_days / len(paid_invoices)
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_aging_report(invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate accounts receivable aging report
        
        Args:
            invoices: List of invoice dictionaries
            
        Returns:
            dict: Aging report by time buckets
        """
        unpaid = [inv for inv in invoices if inv.get('status') not in ['paid', 'cancelled']]
        
        current = []  # 0-30 days
        days_31_60 = []
        days_61_90 = []
        over_90 = []
        
        now = datetime.now()
        
        for inv in unpaid:
            issue_date = inv.get('issue_date')
            if isinstance(issue_date, str):
                issue_date = datetime.fromisoformat(issue_date)
            
            days_old = (now - issue_date).days
            amount = inv.get('total_amount', 0)
            
            if days_old <= 30:
                current.append(inv)
            elif days_old <= 60:
                days_31_60.append(inv)
            elif days_old <= 90:
                days_61_90.append(inv)
            else:
                over_90.append(inv)
        
        return {
            'current': {
                'count': len(current),
                'total': sum(inv.get('total_amount', 0) for inv in current)
            },
            '31_60_days': {
                'count': len(days_31_60),
                'total': sum(inv.get('total_amount', 0) for inv in days_31_60)
            },
            '61_90_days': {
                'count': len(days_61_90),
                'total': sum(inv.get('total_amount', 0) for inv in days_61_90)
            },
            'over_90_days': {
                'count': len(over_90),
                'total': sum(inv.get('total_amount', 0) for inv in over_90)
            },
            'total_outstanding': sum(inv.get('total_amount', 0) for inv in unpaid),
            'total_invoices': len(unpaid)
        }
    
    @staticmethod
    def generate_payment_link(invoice_id: str, 
                            accept_methods: List[str] = None) -> Dict[str, Any]:
        """
        Generate shareable payment link for invoice
        
        Args:
            invoice_id: Invoice identifier
            accept_methods: Accepted payment methods ['ach', 'card', 'wire']
            
        Returns:
            dict: Payment link details
        """
        if accept_methods is None:
            accept_methods = ['ach', 'card']
        
        link = f"https://pay.pulsetrade.com/{invoice_id}"
        short_link = f"https://pt.co/{invoice_id[:8]}"
        
        return {
            'invoice_id': invoice_id,
            'payment_link': link,
            'short_link': short_link,
            'qr_code_url': f"https://api.qrserver.com/v1/create-qr-code/?data={link}",
            'accepted_methods': accept_methods,
            'fees': {
                'ach': 0.0,  # Free ACH
                'card': 2.9,  # 2.9% card fee
                'wire': 0.0   # Free wire
            },
            'expires_at': None,  # No expiration
            'created_at': datetime.now()
        }
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_client_summary(client_id: str, invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get summary of invoicing relationship with client
        
        Args:
            client_id: Client identifier
            invoices: All invoices (will filter by client)
            
        Returns:
            dict: Client invoicing summary
        """
        client_invoices = [inv for inv in invoices if inv.get('client_id') == client_id]
        
        if not client_invoices:
            return {
                'client_id': client_id,
                'total_invoiced': 0,
                'total_paid': 0,
                'total_outstanding': 0,
                'invoice_count': 0,
                'avg_payment_days': 0
            }
        
        total_invoiced = sum(inv.get('total_amount', 0) for inv in client_invoices)
        paid_invoices = [inv for inv in client_invoices if inv.get('status') == 'paid']
        total_paid = sum(inv.get('total_amount', 0) for inv in paid_invoices)
        outstanding = total_invoiced - total_paid
        
        # Calculate average payment time
        payment_days = []
        for inv in paid_invoices:
            if inv.get('payment_date') and inv.get('issue_date'):
                issue = inv['issue_date'] if isinstance(inv['issue_date'], datetime) else datetime.fromisoformat(str(inv['issue_date']))
                paid = inv['payment_date'] if isinstance(inv['payment_date'], datetime) else datetime.fromisoformat(str(inv['payment_date']))
                payment_days.append((paid - issue).days)
        
        avg_payment_days = sum(payment_days) / len(payment_days) if payment_days else 0
        
        return {
            'client_id': client_id,
            'total_invoiced': total_invoiced,
            'total_paid': total_paid,
            'total_outstanding': outstanding,
            'invoice_count': len(client_invoices),
            'paid_count': len(paid_invoices),
            'avg_payment_days': avg_payment_days,
            'payment_reliability': 'excellent' if avg_payment_days < 20 else 'good' if avg_payment_days < 35 else 'fair'
        }

