"""
Government Bank Development Software
Comprehensive banking software for government-owned banks with core banking,
customer management, accounts, and regulatory compliance
"""
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os
import hashlib

class AccountType(Enum):
    """Types of bank accounts"""
    SAVINGS = "बचत खाता (Savings Account)"
    CURRENT = "चालू खाता (Current Account)"
    FIXED_DEPOSIT = "सावधि जमा (Fixed Deposit)"
    RECURRING_DEPOSIT = "आवर्ती जमा (Recurring Deposit)"
    SALARY = "वेतन खाता (Salary Account)"
    OVERDRAFT = "ओवरड्राफ्ट (Overdraft)"
    NRE = "NRE (विदेशी मुद्रा) "
    NRO = "NRO (विदेशी आय)"

class TransactionType(Enum):
    """Types of transactions"""
    DEPOSIT = "जमा (Deposit)"
    WITHDRAWAL = "निकासी (Withdrawal)"
    TRANSFER = "हस्तांतरण (Transfer)"
    CHEQUE_DEPOSIT = "चेक जमा (Cheque Deposit)"
    STANDING_ORDER = "स्थायी आदेश (Standing Order)"
    EMI = "EMI"
    INTEREST = "ब्याज (Interest)"
    SERVICE_CHARGE = "सेवा प्रभार (Service Charge)"
    TAX = "कर (Tax)"

class TransactionStatus(Enum):
    """Status of transactions"""
    INITIATED = "शुरू (Initiated)"
    PENDING = "लंबित (Pending)"
    CLEARED = "समाशोधित (Cleared)"
    REJECTED = "अस्वीकृत (Rejected)"
    REVERSED = "उलटा (Reversed)"

class CustomerType(Enum):
    """Types of bank customers"""
    INDIVIDUAL = "व्यक्तिगत (Individual)"
    CORPORATE = "कॉर्पोरेट (Corporate)"
    GOVERNMENT = "सरकारी (Government)"
    EDUCATIONAL = "शैक्षणिक (Educational)"
    NGO = "NGO"
    PARTNERSHIP = "साझेदारी (Partnership)"
    TRUST = "ट्रस्ट (Trust)"

class LoanStatus(Enum):
    """Status of loans"""
    APPLICATION = "आवेदन (Application)"
    APPROVED = "मंजूर (Approved)"
    SANCTIONED = "अनुमोदित (Sanctioned)"
    DISBURSED = "वितरित (Disbursed)"
    ACTIVE = "सक्रिय (Active)"
    CLOSED = "बंद (Closed)"
    DEFAULT = "डिफ़ॉल्ट (Default)"
    RESTRUCTURED = "पुनर्गठित (Restructured)"

class BranchType(Enum):
    """Types of bank branches"""
    MAIN = "मुख्य (Main)"
    METRO = "मेट्रो (Metro)"
    URBAN = "शहरी (Urban)"
    SEMI_URBAN = "अर्ध-शहरी (Semi-Urban)"
    RURAL = "ग्रामीण (Rural)"

class Customer:
    """Represents a bank customer"""
    
    def __init__(self, customer_id: str, name: str, customer_type: CustomerType,
                 email: str, phone: str, address: str, aadhar: str, pan: str):
        """Initialize a customer"""
        self.customer_id = customer_id
        self.name = name
        self.customer_type = customer_type
        self.email = email
        self.phone = phone
        self.address = address
        self.aadhar = aadhar
        self.pan = pan
        
        self.registration_date = datetime.now()
        self.kyc_status = "Verified"
        self.risk_rating = "Low"
        self.accounts: List[str] = []
        self.total_deposits = 0
        self.total_loans = 0
        self.credit_score = 750
    
    def add_account(self, account_number: str):
        """Add account to customer"""
        if account_number not in self.accounts:
            self.accounts.append(account_number)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'customer_type': self.customer_type.value,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'aadhar': self.aadhar,
            'pan': self.pan,
            'registration_date': self.registration_date.strftime("%d-%m-%Y %H:%M:%S"),
            'kyc_status': self.kyc_status,
            'risk_rating': self.risk_rating,
            'accounts': self.accounts,
            'total_deposits': self.total_deposits,
            'total_loans': self.total_loans,
            'credit_score': self.credit_score
        }
    
    def __str__(self) -> str:
        """String representation"""
        return (f"ग्राहक: {self.name} ({self.customer_id}) | "
                f"{self.customer_type.value} | क्रेडिट स्कोर: {self.credit_score}")


class BankAccount:
    """Represents a bank account"""
    
    def __init__(self, account_number: str, customer: Customer, account_type: AccountType,
                 opening_balance: float, opening_date: str = None):
        """Initialize a bank account"""
        self.account_number = account_number
        self.customer = customer
        self.account_type = account_type
        self.balance = opening_balance
        self.opening_balance = opening_balance
        self.opening_date = opening_date or datetime.now().strftime("%d-%m-%Y")
        self.status = "Active"
        self.interest_rate = self.get_default_rate()
        self.last_transaction_date = None
        self.transactions: List[Dict] = []
        self.service_charge = 0
        self.interest_accrued = 0
        
        customer.add_account(account_number)
    
    def get_default_rate(self) -> float:
        """Get default interest rate based on account type"""
        rates = {
            AccountType.SAVINGS: 3.5,
            AccountType.CURRENT: 0,
            AccountType.FIXED_DEPOSIT: 5.5,
            AccountType.RECURRING_DEPOSIT: 4.0,
            AccountType.SALARY: 3.5,
            AccountType.OVERDRAFT: 10.0,
            AccountType.NRE: 4.0,
            AccountType.NRO: 3.5
        }
        return rates.get(self.account_type, 0)
    
    def deposit(self, amount: float, mode: str = "नकद (Cash)") -> bool:
        """Deposit money"""
        if amount <= 0:
            return False
        
        self.balance += amount
        self.last_transaction_date = datetime.now()
        
        transaction = {
            'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'type': TransactionType.DEPOSIT.value,
            'mode': mode,
            'amount': amount,
            'balance_after': self.balance,
            'status': TransactionStatus.CLEARED.value
        }
        self.transactions.append(transaction)
        return True
    
    def withdraw(self, amount: float, mode: str = "नकद (Cash)") -> bool:
        """Withdraw money"""
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        self.last_transaction_date = datetime.now()
        
        transaction = {
            'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'type': TransactionType.WITHDRAWAL.value,
            'mode': mode,
            'amount': amount,
            'balance_after': self.balance,
            'status': TransactionStatus.CLEARED.value
        }
        self.transactions.append(transaction)
        return True
    
    def transfer_to(self, recipient_account: 'BankAccount', amount: float) -> bool:
        """Transfer funds to another account"""
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        recipient_account.balance += amount
        self.last_transaction_date = datetime.now()
        recipient_account.last_transaction_date = datetime.now()
        
        transaction = {
            'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'type': TransactionType.TRANSFER.value,
            'recipient': recipient_account.account_number,
            'amount': amount,
            'balance_after': self.balance,
            'status': TransactionStatus.CLEARED.value
        }
        self.transactions.append(transaction)
        return True
    
    def calculate_interest(self, days: int = 1) -> float:
        """Calculate daily interest"""
        annual_rate = self.interest_rate / 100
        daily_rate = annual_rate / 365
        interest = self.balance * daily_rate * days
        self.interest_accrued += interest
        return interest
    
    def credit_interest(self):
        """Credit accrued interest to account"""
        if self.interest_accrued > 0:
            self.balance += self.interest_accrued
            
            transaction = {
                'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'type': TransactionType.INTEREST.value,
                'amount': self.interest_accrued,
                'balance_after': self.balance,
                'status': TransactionStatus.CLEARED.value
            }
            self.transactions.append(transaction)
            self.interest_accrued = 0
    
    def deduct_service_charge(self, charge: float):
        """Deduct service charge"""
        if self.balance >= charge:
            self.balance -= charge
            
            transaction = {
                'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'type': TransactionType.SERVICE_CHARGE.value,
                'amount': charge,
                'balance_after': self.balance,
                'status': TransactionStatus.CLEARED.value
            }
            self.transactions.append(transaction)
            return True
        return False
    
    def get_statement(self, days: int = 30) -> List[Dict]:
        """Get account statement for last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        statement = []
        
        for trans in self.transactions:
            trans_date = datetime.strptime(trans['date'], "%d-%m-%Y %H:%M:%S")
            if trans_date >= cutoff_date:
                statement.append(trans)
        
        return statement
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'account_number': self.account_number,
            'customer_id': self.customer.customer_id,
            'account_type': self.account_type.value,
            'balance': self.balance,
            'opening_date': self.opening_date,
            'status': self.status,
            'interest_rate': self.interest_rate,
            'interest_accrued': self.interest_accrued,
            'last_transaction_date': self.last_transaction_date
        }
    
    def __str__(self) -> str:
        """String representation"""
        return (f"खाता: {self.account_number} | {self.account_type.value} | "
                f"शेष: ₹{self.balance:,.2f}")


class Loan:
    """Represents a bank loan"""
    
    def __init__(self, loan_id: str, customer: Customer, principal: float,
                 tenure_months: int, interest_rate: float, purpose: str):
        """Initialize a loan"""
        self.loan_id = loan_id
        self.customer = customer
        self.principal = principal
        self.tenure_months = tenure_months
        self.interest_rate = interest_rate
        self.purpose = purpose
        
        self.status = LoanStatus.APPLICATION
        self.application_date = datetime.now()
        self.approval_date = None
        self.disbursement_date = None
        self.disbursement_account = None
        
        self.total_interest = self.calculate_total_interest()
        self.total_amount = principal + self.total_interest
        self.emi = self.calculate_emi()
        
        self.amount_paid = 0
        self.emi_paid = 0
        self.overdue_amount = 0
        self.emi_schedule: List[Dict] = []
    
    def calculate_total_interest(self) -> float:
        """Calculate total interest"""
        monthly_rate = self.interest_rate / 12 / 100
        total_interest = self.principal * monthly_rate * self.tenure_months
        return total_interest
    
    def calculate_emi(self) -> float:
        """Calculate EMI (Equated Monthly Installment)"""
        monthly_rate = self.interest_rate / 12 / 100
        if monthly_rate == 0:
            return self.principal / self.tenure_months
        
        emi = (self.principal * monthly_rate * (1 + monthly_rate) ** self.tenure_months) / \
              ((1 + monthly_rate) ** self.tenure_months - 1)
        return emi
    
    def approve_loan(self) -> bool:
        """Approve the loan"""
        self.status = LoanStatus.APPROVED
        self.approval_date = datetime.now()
        self.generate_emi_schedule()
        return True
    
    def disburse_loan(self, account: BankAccount) -> bool:
        """Disburse loan to account"""
        self.status = LoanStatus.DISBURSED
        self.disbursement_date = datetime.now()
        self.disbursement_account = account.account_number
        account.deposit(self.principal, "ऋण वितरण (Loan Disbursement)")
        self.customer.total_loans += self.principal
        self.status = LoanStatus.ACTIVE
        return True
    
    def generate_emi_schedule(self):
        """Generate EMI payment schedule"""
        remaining_principal = self.principal
        monthly_rate = self.interest_rate / 12 / 100
        
        for month in range(1, self.tenure_months + 1):
            interest_amount = remaining_principal * monthly_rate
            principal_amount = self.emi - interest_amount
            remaining_principal -= principal_amount
            
            due_date = datetime.now() + timedelta(days=30 * month)
            
            self.emi_schedule.append({
                'month': month,
                'due_date': due_date.strftime("%d-%m-%Y"),
                'emi': self.emi,
                'principal': principal_amount,
                'interest': interest_amount,
                'remaining_balance': max(0, remaining_principal),
                'status': 'Due'
            })
    
    def pay_emi(self, amount: float) -> bool:
        """Pay EMI"""
        if amount < self.emi:
            return False
        
        self.amount_paid += amount
        self.emi_paid += 1
        
        for schedule in self.emi_schedule:
            if schedule['status'] == 'Due':
                schedule['status'] = 'Paid'
                break
        
        if self.emi_paid >= self.tenure_months:
            self.status = LoanStatus.CLOSED
        
        return True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'loan_id': self.loan_id,
            'customer_id': self.customer.customer_id,
            'principal': self.principal,
            'tenure_months': self.tenure_months,
            'interest_rate': self.interest_rate,
            'emi': self.emi,
            'status': self.status.value,
            'application_date': self.application_date.strftime("%d-%m-%Y"),
            'approval_date': self.approval_date.strftime("%d-%m-%Y") if self.approval_date else None,
            'disbursement_date': self.disbursement_date.strftime("%d-%m-%Y") if self.disbursement_date else None,
            'amount_paid': self.amount_paid,
            'emi_paid': self.emi_paid
        }
    
    def __str__(self) -> str:
        """String representation"""
        return (f"ऋण: {self.loan_id} | ग्राहक: {self.customer.name} | "
                f"₹{self.principal:,.0f} @ {self.interest_rate}% | EMI: ₹{self.emi:,.2f}")


class Branch:
    """Represents a bank branch"""
    
    def __init__(self, branch_code: str, branch_name: str, branch_type: BranchType,
                 location: str, ifsc_code: str):
        """Initialize a branch"""
        self.branch_code = branch_code
        self.branch_name = branch_name
        self.branch_type = branch_type
        self.location = location
        self.ifsc_code = ifsc_code
        
        self.establishment_date = datetime.now()
        self.total_customers = 0
        self.total_deposits = 0
        self.total_loans = 0
        self.employees = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'branch_code': self.branch_code,
            'branch_name': self.branch_name,
            'branch_type': self.branch_type.value,
            'location': self.location,
            'ifsc_code': self.ifsc_code,
            'total_customers': self.total_customers,
            'total_deposits': self.total_deposits,
            'total_loans': self.total_loans
        }
    
    def __str__(self) -> str:
        """String representation"""
        return (f"शाखा: {self.branch_name} ({self.branch_code}) | "
                f"{self.branch_type.value} | {self.location}")


class GovernmentBankSystem:
    """Main government bank management system"""
    
    def __init__(self, bank_name: str, bank_code: str, storage_file: str = "govt_bank_data.json"):
        """Initialize government bank system"""
        self.bank_name = bank_name
        self.bank_code = bank_code
        self.storage_file = storage_file
        
        self.customers: List[Customer] = []
        self.accounts: List[BankAccount] = []
        self.loans: List[Loan] = []
        self.branches: List[Branch] = []
        
        self.next_customer_id = 10001
        self.next_account_number = 100000001
        self.next_loan_id = 50001
        
        self.total_deposits = 0
        self.total_loans_outstanding = 0
        self.npa_amount = 0
        
        self.load_data()
    
    def register_customer(self, name: str, customer_type: CustomerType,
                         email: str, phone: str, address: str,
                         aadhar: str, pan: str) -> Optional[Customer]:
        """Register a new customer"""
        customer_id = f"CIF{self.next_customer_id}"
        customer = Customer(customer_id, name, customer_type, email, phone, address, aadhar, pan)
        self.customers.append(customer)
        self.next_customer_id += 1
        print(f"✓ ग्राहक पंजीकृत: {customer.name} ({customer_id})")
        return customer
    
    def find_customer(self, customer_id: str) -> Optional[Customer]:
        """Find customer by ID"""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    def open_account(self, customer_id: str, account_type: AccountType,
                    opening_balance: float = 0) -> Optional[BankAccount]:
        """Open a new account"""
        customer = self.find_customer(customer_id)
        if not customer:
            print(f"✗ ग्राहक {customer_id} नहीं मिला")
            return None
        
        account_number = str(self.next_account_number)
        account = BankAccount(account_number, customer, account_type, opening_balance)
        self.accounts.append(account)
        self.next_account_number += 1
        self.total_deposits += opening_balance
        print(f"✓ खाता खोला गया: {account_number} - {account_type.value}")
        return account
    
    def find_account(self, account_number: str) -> Optional[BankAccount]:
        """Find account by number"""
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None
    
    def apply_for_loan(self, customer_id: str, principal: float,
                      tenure_months: int, interest_rate: float,
                      purpose: str) -> Optional[Loan]:
        """Apply for a loan"""
        customer = self.find_customer(customer_id)
        if not customer:
            print(f"✗ ग्राहक {customer_id} नहीं मिला")
            return None
        
        loan_id = f"LN{self.next_loan_id}"
        loan = Loan(loan_id, customer, principal, tenure_months, interest_rate, purpose)
        self.loans.append(loan)
        self.next_loan_id += 1
        print(f"✓ ऋण आवेदन: {loan_id} - ₹{principal:,.0f}")
        return loan
    
    def approve_and_disburse_loan(self, loan_id: str, account_number: str) -> bool:
        """Approve and disburse loan"""
        loan = None
        for l in self.loans:
            if l.loan_id == loan_id:
                loan = l
                break
        
        if not loan:
            print(f"✗ ऋण {loan_id} नहीं मिला")
            return False
        
        account = self.find_account(account_number)
        if not account:
            print(f"✗ खाता {account_number} नहीं मिला")
            return False
        
        loan.approve_loan()
        loan.disburse_loan(account)
        self.total_loans_outstanding += loan.principal
        print(f"✓ ऋण मंजूर और वितरित: {loan_id}")
        return True
    
    def create_branch(self, branch_code: str, branch_name: str,
                     branch_type: BranchType, location: str, ifsc_code: str) -> Optional[Branch]:
        """Create a new branch"""
        branch = Branch(branch_code, branch_name, branch_type, location, ifsc_code)
        self.branches.append(branch)
        print(f"✓ शाखा खोली गई: {branch_name} ({branch_code})")
        return branch
    
    def get_branch_summary(self, branch_code: str) -> Dict:
        """Get branch summary"""
        branch = None
        for b in self.branches:
            if b.branch_code == branch_code:
                branch = b
                break
        
        if not branch:
            return {}
        
        return branch.to_dict()
    
    def calculate_npa(self) -> float:
        """Calculate Non-Performing Assets (NPA)"""
        npa = 0
        for loan in self.loans:
            if loan.status == LoanStatus.DEFAULT:
                npa += loan.principal - loan.amount_paid
        return npa
    
    def get_financial_summary(self) -> Dict:
        """Get financial summary"""
        total_deposits = sum(account.balance for account in self.accounts)
        total_loans = sum(loan.principal for loan in self.loans if loan.status == LoanStatus.ACTIVE)
        npa = self.calculate_npa()
        
        return {
            'total_customers': len(self.customers),
            'total_accounts': len(self.accounts),
            'total_deposits': total_deposits,
            'total_loans_outstanding': total_loans,
            'total_loans_applications': len(self.loans),
            'npa_amount': npa,
            'npa_percentage': (npa / total_loans * 100) if total_loans > 0 else 0,
            'capital_deposits_ratio': (total_deposits / (total_deposits + total_loans)) if (total_deposits + total_loans) > 0 else 0
        }
    
    def display_dashboard(self):
        """Display banking dashboard"""
        summary = self.get_financial_summary()
        
        print("\n" + "="*100)
        print(f"🏛️ {self.bank_name.upper()} - बैंकिंग डैशबोर्ड (BANKING DASHBOARD)")
        print(f"बैंक कोड: {self.bank_code}")
        print("="*100)
        
        print("\n👥 ग्राहक और खाते (CUSTOMERS & ACCOUNTS):")
        print(f"  कुल ग्राहक (Total Customers):      {summary['total_customers']}")
        print(f"  कुल खाते (Total Accounts):          {summary['total_accounts']}")
        print(f"  कुल शाखाएं (Total Branches):       {len(self.branches)}")
        
        print("\n💰 जमा और ऋण (DEPOSITS & LOANS):")
        print(f"  कुल जमा (Total Deposits):           ₹{summary['total_deposits']:>15,.2f}")
        print(f"  कुल बकाया ऋण (Total Loans):        ₹{summary['total_loans_outstanding']:>15,.2f}")
        print(f"  ऋण आवेदन (Loan Applications):     {summary['total_loans_applications']}")
        
        print("\n📊 जोखिम प्रबंधन (RISK MANAGEMENT):")
        print(f"  NPA राशि (NPA Amount):              ₹{summary['npa_amount']:>15,.2f}")
        print(f"  NPA प्रतिशत (NPA %):                {summary['npa_percentage']:>15,.2f}%")
        print(f"  पूंजी-जमा अनुपात (CD Ratio):        {summary['capital_deposits_ratio']:>15,.2f}%")
        
        print("\n🏢 शाखा विवरण (BRANCH DETAILS):")
        for branch in self.branches:
            print(f"  {branch.branch_name} ({branch.branch_code}) - {branch.branch_type.value}")
        
        print("="*100 + "\n")
    
    def generate_report(self, report_type: str) -> Dict:
        """Generate various reports"""
        if report_type == "financial":
            return self.get_financial_summary()
        elif report_type == "customers":
            return {
                'total_customers': len(self.customers),
                'individuals': sum(1 for c in self.customers if c.customer_type == CustomerType.INDIVIDUAL),
                'corporate': sum(1 for c in self.customers if c.customer_type == CustomerType.CORPORATE),
                'government': sum(1 for c in self.customers if c.customer_type == CustomerType.GOVERNMENT)
            }
        elif report_type == "loans":
            return {
                'total_applications': len(self.loans),
                'approved': sum(1 for l in self.loans if l.status == LoanStatus.APPROVED),
                'active': sum(1 for l in self.loans if l.status == LoanStatus.ACTIVE),
                'closed': sum(1 for l in self.loans if l.status == LoanStatus.CLOSED),
                'default': sum(1 for l in self.loans if l.status == LoanStatus.DEFAULT)
            }
        return {}
    
    def save_data(self) -> bool:
        """Save all data to file"""
        try:
            data = {
                'bank_name': self.bank_name,
                'bank_code': self.bank_code,
                'customers': [c.to_dict() for c in self.customers],
                'accounts': [a.to_dict() for a in self.accounts],
                'loans': [l.to_dict() for l in self.loans],
                'branches': [b.to_dict() for b in self.branches],
                'last_saved': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ डेटा सहेजा गया: {self.storage_file}")
            return True
        except Exception as e:
            print(f"✗ डेटा सहेजने में त्रुटि: {str(e)}")
            return False
    
    def load_data(self) -> bool:
        """Load data from file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✓ डेटा लोड किया गया: {self.storage_file}")
                return True
            return True
        except Exception as e:
            print(f"✗ डेटा लोड करने में त्रुटि: {str(e)}")
            return False


# Demo and Example Usage
if __name__ == "__main__":
    print("\n" + "="*100)
    print("🏛️ भारतीय सरकारी बैंक प्रबंधन प्रणाली")
    print("GOVERNMENT BANK DEVELOPMENT SOFTWARE - DEMO MODE")
    print("="*100 + "\n")
    
    # Initialize bank
    bank = GovernmentBankSystem("भारतीय स्टेट बैंक (State Bank of India)", "SBIN0000001")
    
    # Create branches
    print("🏢 शाखाएं खोली जा रही हैं (Creating Branches)...\n")
    main_branch = bank.create_branch("SBIN0001", "मुख्य शाखा, मुंबई", BranchType.MAIN, "मुंबई, महाराष्ट्र", "SBIN0001001")
    metro_branch = bank.create_branch("SBIN0002", "मेट्रो शाखा, दिल्ली", BranchType.METRO, "नई दिल्ली", "SBIN0002001")
    
    # Register customers
    print("\n👥 ग्राहकों को पंजीकृत किया जा रहा है (Registering Customers)...\n")
    cust1 = bank.register_customer(
        "राजीव कुमार",
        CustomerType.INDIVIDUAL,
        "rajiv@email.com",
        "9876543210",
        "मुंबई, महाराष्ट्र",
        "1234-5678-9012-3456",
        "ABCDE1234F"
    )
    
    cust2 = bank.register_customer(
        "प्रियंका शर्मा",
        CustomerType.CORPORATE,
        "priyanka@company.com",
        "9987654321",
        "बैंगलोर, कर्नाटक",
        "9876-5432-1098-7654",
        "XYZAB5678G"
    )
    
    cust3 = bank.register_customer(
        "अजय पटेल",
        CustomerType.INDIVIDUAL,
        "ajay@email.com",
        "9876543212",
        "दिल्ली",
        "5555-6666-7777-8888",
        "PQRST9012H"
    )
    
    # Open accounts
    print("\n💳 खाते खोले जा रहे हैं (Opening Accounts)...\n")
    acc1 = bank.open_account(cust1.customer_id, AccountType.SAVINGS, 50000)
    acc2 = bank.open_account(cust1.customer_id, AccountType.FIXED_DEPOSIT, 100000)
    acc3 = bank.open_account(cust2.customer_id, AccountType.CURRENT, 500000)
    acc4 = bank.open_account(cust3.customer_id, AccountType.SALARY, 75000)
    
    # Perform transactions
    print("\n💳 लेनदेन किए जा रहे हैं (Performing Transactions)...\n")
    acc1.deposit(25000, "चेक (Cheque)")
    print(f"  ✓ जमा: ₹25,000 | शेष: ₹{acc1.balance:,.2f}")
    
    acc1.withdraw(10000, "नकद (Cash)")
    print(f"  ✓ निकासी: ₹10,000 | शेष: ₹{acc1.balance:,.2f}")
    
    acc1.transfer_to(acc3, 5000)
    print(f"  ✓ हस्तांतरण: ₹5,000 से {acc1.account_number} से {acc3.account_number}")
    
    # Apply for loans
    print("\n📋 ऋण के लिए आवेदन किए जा रहे हैं (Applying for Loans)...\n")
    loan1 = bank.apply_for_loan(cust1.customer_id, 500000, 60, 8.5, "होम लोन (Home Loan)")
    loan2 = bank.apply_for_loan(cust2.customer_id, 2000000, 84, 7.5, "बिजनेस लोन (Business Loan)")
    
    # Approve and disburse loans
    print("\n✅ ऋण स्वीकृत और वितरित किए जा रहे हैं (Approving & Disbursing Loans)...\n")
    bank.approve_and_disburse_loan(loan1.loan_id, acc1.account_number)
    bank.approve_and_disburse_loan(loan2.loan_id, acc3.account_number)
    
    # Calculate interest
    print("\n📊 ब्याज की गणना की जा रही है (Calculating Interest)...\n")
    interest = acc1.calculate_interest(30)
    print(f"  ✓ 30 दिनों का ब्याज: ₹{interest:,.2f}")
    acc1.credit_interest()
    print(f"  ✓ ब्याज क्रेडिट किया गया | नया शेष: ₹{acc1.balance:,.2f}")
    
    # Display account statement
    print("\n📄 खाता विवरण (Account Statement)...\n")
    statement = acc1.get_statement(days=30)
    print(f"खाता {acc1.account_number} - पिछले 30 दिनों के लेनदेन:")
    for trans in statement:
        print(f"  {trans['date']} | {trans['type']} | ₹{trans.get('amount', trans.get('balance_after', 0)):>10,.2f}")
    
    # Display dashboard
    bank.display_dashboard()
    
    # Generate reports
    print("\n📊 विभिन्न रिपोर्ट्स (Generating Reports)...\n")
    print("वित्तीय रिपोर्ट (Financial Report):")
    fin_report = bank.generate_report("financial")
    for key, value in fin_report.items():
        if isinstance(value, float):
            print(f"  {key}: ₹{value:,.2f}")
        else:
            print(f"  {key}: {value}")
    
    print("\nऋण रिपोर्ट (Loan Report):")
    loan_report = bank.generate_report("loans")
    for key, value in loan_report.items():
        print(f"  {key}: {value}")
    
    # Save data
    print("\n💾 डेटा सहेजा जा रहा है (Saving Data)...\n")
    bank.save_data()
    
    print("\n✓ डेमो सफल रहा! (Demo Completed Successfully!)")
    print("="*100 + "\n")
