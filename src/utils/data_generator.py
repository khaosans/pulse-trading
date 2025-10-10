"""
Synthetic Data Generator for Banking and Freelancer Features
Generates realistic demo data for accounts, transactions, invoices, expenses, taxes
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from dataclasses import dataclass, asdict
import streamlit as st

@dataclass
class BankAccount:
    """Bank account information"""
    account_id: str
    account_number: str
    routing_number: str
    account_type: str  # 'checking', 'savings', 'tax_pot'
    balance: float
    available_balance: float
    currency: str = 'USD'
    status: str = 'active'

@dataclass
class Transaction:
    """Bank transaction"""
    transaction_id: str
    date: datetime
    description: str
    amount: float
    transaction_type: str  # 'debit', 'credit'
    category: str
    status: str  # 'pending', 'completed', 'failed'
    balance_after: float

@dataclass
class Invoice:
    """Client invoice"""
    invoice_id: str
    client_name: str
    client_email: str
    issue_date: datetime
    due_date: datetime
    amount: float
    tax_amount: float
    total_amount: float
    status: str  # 'draft', 'sent', 'viewed', 'paid', 'overdue'
    payment_date: Optional[datetime]
    line_items: List[Dict[str, Any]]
    payment_method: Optional[str]  # 'ach', 'card', 'wire'

@dataclass
class Expense:
    """Business expense"""
    expense_id: str
    date: datetime
    merchant: str
    description: str
    amount: float
    category: str
    tax_deductible: bool
    receipt_url: Optional[str]
    payment_method: str  # 'card', 'ach', 'cash'

class DataGenerator:
    """Generates realistic synthetic data for banking and freelancer features"""
    
    # Realistic client names for invoicing
    CLIENT_NAMES = [
        "Acme Corporation", "TechStart Inc", "Global Designs LLC", 
        "Innovation Labs", "Digital Ventures", "Creative Studios",
        "Enterprise Solutions", "Startup Hub", "Cloud Services Co",
        "Marketing Pros", "Design Agency", "Dev Shop Inc"
    ]
    
    # Expense categories for freelancers
    EXPENSE_CATEGORIES = {
        "Software & Tools": ["Adobe Creative Cloud", "Figma Pro", "GitHub", "Notion", "Slack Premium"],
        "Office Supplies": ["Notebooks", "Pens", "Monitor", "Keyboard", "Mouse"],
        "Internet & Phone": ["Internet Service", "Mobile Phone", "Cloud Storage"],
        "Professional Services": ["Accountant", "Legal Fees", "Business Insurance"],
        "Marketing": ["LinkedIn Ads", "Google Ads", "Business Cards", "Website Hosting"],
        "Education": ["Course: Advanced React", "Conference Ticket", "Book: Design Patterns"],
        "Travel": ["Client Meeting Travel", "Conference Flight", "Hotel"],
        "Meals & Entertainment": ["Client Lunch", "Team Dinner", "Coffee Meeting"]
    }
    
    @staticmethod
    @st.cache_data
    def generate_bank_account() -> Dict[str, Any]:
        """Generate a realistic bank account"""
        account = BankAccount(
            account_id="acc_" + ''.join(random.choices('0123456789', k=12)),
            account_number=''.join(random.choices('0123456789', k=12)),
            routing_number=''.join(random.choices('0123456789', k=9)),
            account_type='checking',
            balance=random.uniform(5000, 50000),
            available_balance=0,  # Will calculate
            currency='USD',
            status='active'
        )
        account.available_balance = account.balance - random.uniform(0, 1000)
        return asdict(account)
    
    @staticmethod
    @st.cache_data
    def generate_tax_pot_account(balance: float = None) -> Dict[str, Any]:
        """Generate tax savings account"""
        if balance is None:
            balance = random.uniform(2000, 15000)
        
        account = BankAccount(
            account_id="tax_" + ''.join(random.choices('0123456789', k=12)),
            account_number=''.join(random.choices('0123456789', k=12)),
            routing_number=''.join(random.choices('0123456789', k=9)),
            account_type='tax_pot',
            balance=balance,
            available_balance=balance,
            currency='USD',
            status='active'
        )
        return asdict(account)
    
    @staticmethod
    @st.cache_data(ttl=300)
    def generate_transactions(num_transactions: int = 30) -> pd.DataFrame:
        """Generate realistic transaction history"""
        transactions = []
        balance = random.uniform(20000, 40000)
        
        for i in range(num_transactions):
            # Mix of income (invoice payments) and expenses
            is_income = random.random() < 0.4  # 40% income, 60% expenses
            
            if is_income:
                amount = random.uniform(500, 5000)
                description = f"Invoice Payment - {random.choice(DataGenerator.CLIENT_NAMES)}"
                transaction_type = 'credit'
                category = 'Income'
            else:
                amount = -random.uniform(50, 800)
                category = random.choice(list(DataGenerator.EXPENSE_CATEGORIES.keys()))
                merchants = DataGenerator.EXPENSE_CATEGORIES[category]
                description = random.choice(merchants)
                transaction_type = 'debit'
            
            balance += amount
            
            transaction = Transaction(
                transaction_id=f"txn_{i:08d}",
                date=datetime.now() - timedelta(days=num_transactions-i),
                description=description,
                amount=amount,
                transaction_type=transaction_type,
                category=category,
                status=random.choice(['completed'] * 9 + ['pending']),  # 90% completed
                balance_after=balance
            )
            transactions.append(asdict(transaction))
        
        return pd.DataFrame(transactions)
    
    @staticmethod
    @st.cache_data(ttl=300)
    def generate_invoices(num_invoices: int = 10) -> pd.DataFrame:
        """Generate realistic invoices with various statuses"""
        invoices = []
        
        for i in range(num_invoices):
            issue_date = datetime.now() - timedelta(days=random.randint(1, 90))
            due_date = issue_date + timedelta(days=random.choice([15, 30, 45]))
            
            # Generate line items
            num_items = random.randint(1, 4)
            line_items = []
            subtotal = 0
            
            services = [
                "Website Design", "Logo Design", "UI/UX Design",
                "Web Development", "App Development", "API Integration",
                "Consulting Services", "Strategy Session", "Code Review",
                "Content Writing", "Copywriting", "SEO Optimization"
            ]
            
            for _ in range(num_items):
                hours = random.randint(5, 40)
                rate = random.choice([75, 100, 125, 150, 175, 200])
                item_total = hours * rate
                subtotal += item_total
                
                line_items.append({
                    'description': random.choice(services),
                    'hours': hours,
                    'rate': rate,
                    'amount': item_total
                })
            
            tax_amount = subtotal * 0.0  # No sales tax for most freelance services
            total_amount = subtotal + tax_amount
            
            # Determine status based on dates
            days_since_issue = (datetime.now() - issue_date).days
            days_until_due = (due_date - datetime.now()).days
            
            if days_since_issue < 2:
                status = 'sent'
                payment_date = None
                payment_method = None
            elif days_since_issue < 5 and random.random() < 0.3:
                status = 'viewed'
                payment_date = None
                payment_method = None
            elif days_until_due < 0 and random.random() < 0.3:
                status = 'overdue'
                payment_date = None
                payment_method = None
            elif random.random() < 0.6:
                status = 'paid'
                payment_date = issue_date + timedelta(days=random.randint(5, 25))
                payment_method = random.choice(['ach', 'card', 'wire'])
            else:
                status = 'sent'
                payment_date = None
                payment_method = None
            
            client_name = random.choice(DataGenerator.CLIENT_NAMES)
            
            invoice = Invoice(
                invoice_id=f"INV-{1000+i}",
                client_name=client_name,
                client_email=client_name.lower().replace(' ', '.') + '@example.com',
                issue_date=issue_date,
                due_date=due_date,
                amount=subtotal,
                tax_amount=tax_amount,
                total_amount=total_amount,
                status=status,
                payment_date=payment_date,
                line_items=line_items,
                payment_method=payment_method
            )
            invoices.append(asdict(invoice))
        
        return pd.DataFrame(invoices)
    
    @staticmethod
    @st.cache_data(ttl=300)
    def generate_expenses(num_expenses: int = 30) -> pd.DataFrame:
        """Generate realistic business expenses"""
        expenses = []
        
        for i in range(num_expenses):
            category = random.choice(list(DataGenerator.EXPENSE_CATEGORIES.keys()))
            merchant = random.choice(DataGenerator.EXPENSE_CATEGORIES[category])
            
            # Amount varies by category
            amount_ranges = {
                "Software & Tools": (20, 200),
                "Office Supplies": (10, 500),
                "Internet & Phone": (50, 150),
                "Professional Services": (200, 2000),
                "Marketing": (50, 500),
                "Education": (30, 500),
                "Travel": (100, 1500),
                "Meals & Entertainment": (20, 200)
            }
            
            min_amt, max_amt = amount_ranges.get(category, (20, 200))
            amount = random.uniform(min_amt, max_amt)
            
            # Most expenses are tax deductible
            tax_deductible = category not in ['Meals & Entertainment'] or random.random() < 0.5
            
            expense = Expense(
                expense_id=f"exp_{i:06d}",
                date=datetime.now() - timedelta(days=random.randint(1, 60)),
                merchant=merchant,
                description=f"{merchant} - {category}",
                amount=amount,
                category=category,
                tax_deductible=tax_deductible,
                receipt_url=f"/receipts/receipt_{i:06d}.pdf" if random.random() < 0.7 else None,
                payment_method=random.choice(['card', 'ach'] * 4 + ['cash'])
            )
            expenses.append(asdict(expense))
        
        df = pd.DataFrame(expenses)
        df = df.sort_values('date', ascending=False)
        return df
    
    @staticmethod
    @st.cache_data
    def generate_tax_estimates(income: float = None, expenses: float = None) -> Dict[str, Any]:
        """Generate tax estimates based on income and expenses"""
        if income is None:
            income = random.uniform(60000, 150000)
        
        if expenses is None:
            expenses = income * random.uniform(0.15, 0.35)
        
        taxable_income = income - expenses
        
        # Simplified tax calculation (federal + state + self-employment)
        # Federal: progressive rates (simplified)
        if taxable_income <= 44625:
            federal_rate = 0.12
        elif taxable_income <= 95375:
            federal_rate = 0.22
        else:
            federal_rate = 0.24
        
        federal_tax = taxable_income * federal_rate
        
        # State tax (average ~5%)
        state_tax = taxable_income * 0.05
        
        # Self-employment tax (15.3% on 92.35% of net income)
        se_tax = (income - expenses) * 0.9235 * 0.153
        
        total_tax = federal_tax + state_tax + se_tax
        
        # Quarterly estimates
        quarterly = total_tax / 4
        
        # Next quarterly due dates
        today = datetime.now()
        quarterly_dates = [
            datetime(today.year, 4, 15),  # Q1
            datetime(today.year, 6, 15),  # Q2
            datetime(today.year, 9, 15),  # Q3
            datetime(today.year + 1, 1, 15),  # Q4
        ]
        
        next_due = next((d for d in quarterly_dates if d > today), quarterly_dates[0])
        
        return {
            'gross_income': income,
            'deductible_expenses': expenses,
            'taxable_income': taxable_income,
            'federal_tax': federal_tax,
            'state_tax': state_tax,
            'self_employment_tax': se_tax,
            'total_estimated_tax': total_tax,
            'quarterly_payment': quarterly,
            'next_due_date': next_due,
            'effective_tax_rate': (total_tax / income * 100) if income > 0 else 0,
            'recommended_savings_pct': 30  # Save 30% for taxes
        }
    
    @staticmethod
    @st.cache_data
    def generate_clients(num_clients: int = 10) -> pd.DataFrame:
        """Generate client database with contact info and history"""
        clients = []
        
        for i, name in enumerate(DataGenerator.CLIENT_NAMES[:num_clients]):
            clients.append({
                'client_id': f"client_{i:04d}",
                'name': name,
                'email': name.lower().replace(' ', '.') + '@example.com',
                'phone': f"+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}",
                'total_invoiced': random.uniform(5000, 50000),
                'total_paid': random.uniform(4000, 45000),
                'outstanding': random.uniform(0, 5000),
                'num_projects': random.randint(2, 15),
                'avg_payment_days': random.randint(10, 45),
                'status': random.choice(['active'] * 8 + ['inactive'] * 2),
                'first_project_date': datetime.now() - timedelta(days=random.randint(30, 730)),
                'last_project_date': datetime.now() - timedelta(days=random.randint(1, 60))
            })
        
        return pd.DataFrame(clients)

